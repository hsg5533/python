import sys
import feedparser        # RSS 피드 파싱용 라이브러리
import numpy as np       # 수치 계산용 라이브러리
import tensorflow as tf  # TensorFlow 라이브러리 (모델 로딩 및 연산)
import tensorflow_hub as hub  # TensorFlow Hub에서 모델 불러오기용 라이브러리
import fitz              # PyMuPDF: PDF 파일에서 텍스트 추출용
import re
import requests          # 텔레그램 API 호출용

from urllib.parse import quote

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QListWidget, QSplitter, QFileDialog, QProgressBar
)
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView  # 웹 페이지 렌더링 위젯

# 텔레그램 봇 정보 (실제 값으로 변경)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def load_pdf_text(pdf_path):
    """
    주어진 PDF 파일에서 텍스트를 추출하는 함수.
    PyMuPDF(fitz)를 사용하여 PDF의 모든 페이지 텍스트를 누적합니다.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"PDF 로딩 오류: {e}")
        return ""

def cosine_similarity(a, b):
    """
    두 벡터 a와 b 사이의 코사인 유사도를 계산하는 함수.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def extract_company_name(text):
    """
    PDF 텍스트에서 회사명을 추출하는 함수.
    여러 정규표현식 패턴을 적용하여 '회사명:', '주식회사', '유한회사' 등의 패턴에서 회사명을 파악합니다.
    추출에 실패하면 첫 번째 문장을 반환합니다.
    """
    patterns = [
        r"회사명[:：]\s*([^\n,，]+)",
        r"주식회사\s*([^\n,，]+)",
        r"유한회사\s*([^\n,，]+)",
        r"([^\n,，]+)\s*주식회사",
        r"([^\n,，]+)\s*유한회사"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            company = match.group(1).strip()
            print("추출된 회사명:", company)
            return company
    sentences = re.split(r'[.?!]\s+', text)
    if sentences:
        company = sentences[0].strip()
        print("첫 문장을 회사명으로 사용:", company)
        return company
    return ""

def send_telegram_message(message, bot_token, chat_id):
    """
    텔레그램 API를 사용하여 메시지를 전송합니다.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, data=payload)
    print("텔레그램 전송 응답:", response.json())
    return response.json()

def sanitize_keyword(keyword):
    """
    제어문자(개행 등)를 제거하고 URL 인코딩된 문자열을 반환합니다.
    """
    sanitized_keyword = re.sub(r'[\r\n]+', ' ', keyword).strip()
    return quote(sanitized_keyword)

class PDFEmbeddingWorker(QThread):
    finished = pyqtSignal(list)  # 계산 완료 시 pdf_data 리스트 전달

    def __init__(self, file_paths, embed):
        super().__init__()
        self.file_paths = file_paths
        self.embed = embed

    def run(self):
        pdf_data = []
        for file_path in self.file_paths:
            text = load_pdf_text(file_path)
            if text:
                global_embedding = self.embed([text])[0]
                sentences = re.split(r'[.?!]\s+', text)
                sentences = [s.strip() for s in sentences if s.strip()]
                if sentences:
                    sentence_embeddings = self.embed(sentences)
                    print(f"{file_path}: 총 {len(sentences)}개의 문장 임베딩 업데이트 완료.")
                else:
                    sentence_embeddings = None
                    print(f"{file_path}: 문장을 추출하지 못했습니다.")
                pdf_data.append({
                    'file_path': file_path,
                    'text': text,
                    'global_embedding': global_embedding,
                    'sentence_embeddings': sentence_embeddings
                })
            else:
                print(f"{file_path}에서 텍스트 추출 실패.")
        self.finished.emit(pdf_data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("구글 뉴스 RSS 검색기 (회사 관련 뉴스 필터링)")
        self.setGeometry(200, 200, 1200, 700)

        # ───────────────────────────────────────────────
        # (1) TensorFlow Hub 모델 로딩 및 데이터 초기화
        # ───────────────────────────────────────────────
        print("TensorFlow Hub 모델 로딩 중...")
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        print("모델 로드 완료.")
        self.pdf_data = []  # 여러 PDF 파일의 데이터를 저장

        # ───────────────────────────────────────────────
        # (2) UI 구성
        # ───────────────────────────────────────────────
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # PDF 파일 업로드 영역
        company_layout = QHBoxLayout()
        company_label = QLabel("회사소개서 PDF 파일:")
        self.company_file_line = QLineEdit()
        self.company_file_line.setReadOnly(True)
        self.upload_button = QPushButton("파일 선택")
        self.upload_button.clicked.connect(self.upload_pdf)
        company_layout.addWidget(company_label)
        company_layout.addWidget(self.company_file_line)
        company_layout.addWidget(self.upload_button)
        main_layout.addLayout(company_layout)

        # 진행률 표시 (PDF 임베딩 계산 중)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 뉴스 검색 입력 영역 (검색어 미입력 시 PDF에서 자동으로 회사명 추출)
        top_layout = QHBoxLayout()
        self.keyword_label = QLabel("검색어:")
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("예: 테슬라, 아이폰 ...")
        self.region_label = QLabel("지역:")
        self.region_combo = QComboBox()
        self.region_combo.addItem("한국 (ko)", ("ko", "KR", "KR:ko"))
        self.region_combo.addItem("미국 (en)", ("en", "US", "US:en"))
        self.region_combo.addItem("일본 (ja)", ("ja", "JP", "JP:ja"))
        self.region_combo.addItem("영국 (en-GB)", ("en-GB", "GB", "GB:en-GB"))
        self.region_combo.addItem("프랑스 (fr)", ("fr", "FR", "FR:fr"))
        self.search_button = QPushButton("검색")
        self.search_button.clicked.connect(self.fetch_news)
        top_layout.addWidget(self.keyword_label)
        top_layout.addWidget(self.keyword_input)
        top_layout.addWidget(self.region_label)
        top_layout.addWidget(self.region_combo)
        top_layout.addWidget(self.search_button)
        main_layout.addLayout(top_layout)

        # 뉴스 리스트와 상세보기 영역 (Splitter 사용)
        splitter = QSplitter(Qt.Horizontal)
        self.news_list = QListWidget()
        self.news_list.currentRowChanged.connect(self.show_selected_news_detail)
        self.detail_view = QWebEngineView()
        self.detail_view.setMinimumSize(600, 400)
        splitter.addWidget(self.news_list)
        splitter.addWidget(self.detail_view)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 7)
        splitter.setSizes([300, 900])
        main_layout.addWidget(splitter)

        self.articles = []

    def upload_pdf(self):
        """
        파일 다이얼로그를 열어 여러 PDF 파일을 선택한 후,
        백그라운드 스레드(PDFEmbeddingWorker)를 통해 각 PDF의 임베딩을 계산합니다.
        """
        file_paths, _ = QFileDialog.getOpenFileNames(self, "PDF 파일 선택", "", "PDF Files (*.pdf)")
        if file_paths:
            self.company_file_line.setText("; ".join(file_paths))
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # 진행률 무한대
            self.worker = PDFEmbeddingWorker(file_paths, self.embed)
            self.worker.finished.connect(self.on_pdf_embeddings_finished)
            self.worker.start()

    def on_pdf_embeddings_finished(self, pdf_data):
        """
        PDFEmbeddingWorker 작업 완료 후 호출되는 슬롯.
        """
        self.pdf_data = pdf_data
        self.progress_bar.setVisible(False)
        if self.pdf_data:
            print("모든 PDF 파일 업로드 및 임베딩 업데이트 완료.")
        else:
            print("선택한 PDF들에서 텍스트 추출 실패.")

    def compute_composite_similarity(self, news_embedding):
        """
        뉴스 제목 임베딩과 각 PDF의 임베딩 간의 복합 코사인 유사도를 계산합니다.
        1. 글로벌 유사도, 2. 최고 문장 유사도, 3. 유효 문장 평균 유사도를 가중 평균하여 최종 점수를 산출합니다.
        """
        news_emb_np = news_embedding.numpy()
        best_composite = -1.0
        best_pdf = "N/A"
        threshold = 0.15
        for pdf in self.pdf_data:
            global_emb_np = pdf['global_embedding'].numpy()
            global_sim = cosine_similarity(global_emb_np, news_emb_np)
            composite_sim = global_sim
            if pdf['sentence_embeddings'] is not None:
                sentence_emb_np = pdf['sentence_embeddings'].numpy()
                norms = np.linalg.norm(sentence_emb_np, axis=1)
                news_norm = np.linalg.norm(news_emb_np)
                sentence_sims = np.dot(sentence_emb_np, news_emb_np) / (norms * news_norm)
                top_sentence_sim = np.max(sentence_sims)
                valid_sentences = sentence_sims[sentence_sims > threshold]
                avg_valid_sim = np.mean(valid_sentences) if valid_sentences.size > 0 else 0
                composite_sim = 0.3 * global_sim + 0.4 * top_sentence_sim + 0.3 * avg_valid_sim
            if composite_sim > best_composite:
                best_composite = composite_sim
                best_pdf = pdf['file_path']
        return best_composite, best_pdf

    def build_rss_url(self, keyword, hl, gl, ceid):
        """
        검색어와 지역 정보를 사용하여 구글 뉴스 RSS URL을 생성합니다.
        검색어 내 제어문자를 제거하고 URL 인코딩합니다.
        """
        encoded_keyword = sanitize_keyword(keyword)
        base_url = "https://news.google.com/rss/search"
        return f"{base_url}?q={encoded_keyword}&hl={hl}&gl={gl}&ceid={ceid}"

    def send_top_articles_via_telegram(self, top_n=3):
        """
        검색 결과에서 복합 유사도가 높은 상위 몇 개의 뉴스를 선택하여 텔레그램 메시지로 전송합니다.
        """
        if not self.articles:
            print("발송할 뉴스 기사가 없습니다.")
            return

        sorted_articles = sorted(self.articles, key=lambda x: x['similarity'], reverse=True)
        top_articles = sorted_articles[:top_n]
        message_lines = ["<b>Top Similar News Articles:</b>"]
        for idx, article in enumerate(top_articles, start=1):
            line = (f"{idx}. {article['title']} (sim={article['similarity']:.2f})\n"
                    f"Link: {article['link']}")
            message_lines.append(line)
        message = "\n\n".join(message_lines)
        send_telegram_message(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    def fetch_news(self):
        """
        업로드된 PDF 파일에서 자동으로 회사명을 추출하여 검색어로 사용하고,
        구글 뉴스 RSS 피드를 가져와 각 뉴스의 복합 유사도를 계산합니다.
        이후 상위 결과를 텔레그램으로 전송합니다.
        """
        keyword = self.keyword_input.text().strip()
        if not keyword:
            if self.pdf_data:
                keyword = extract_company_name(self.pdf_data[0]['text'])
            else:
                self.detail_view.setHtml(
                    "<html><head><meta charset='UTF-8'></head><body><p>회사소개서 PDF 파일이 업로드되지 않았습니다.</p></body></html>",
                    QUrl("about:blank")
                )
                return

        hl, gl, ceid = self.region_combo.currentData()
        rss_url = self.build_rss_url(keyword, hl, gl, ceid)
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            self.news_list.clear()
            self.detail_view.setHtml(
                "<html><head><meta charset='UTF-8'></head><body><p>검색 결과가 없습니다.</p></body></html>",
                QUrl("about:blank")
            )
            return

        self.news_list.clear()
        self.articles = []
        similarity_threshold = 0.2  # 임계값

        for entry in feed.entries:
            title = entry.title
            link = entry.link
            published = getattr(entry, 'published', '발행 일자 없음')
            news_embedding = self.embed([title])[0]
            similarity, best_pdf = self.compute_composite_similarity(news_embedding)
            print(f"뉴스: {title} / 복합 유사도: {similarity:.2f} / Best PDF: {best_pdf}")
            if similarity >= similarity_threshold:
                article_info = {
                    'title': title,
                    'link': link,
                    'published': published,
                    'similarity': similarity,
                    'best_pdf': best_pdf
                }
                self.articles.append(article_info)
                self.news_list.addItem(f"[{len(self.articles)}] {title} (sim={similarity:.2f})")
        if not self.articles:
            self.detail_view.setHtml(
                "<html><head><meta charset='UTF-8'></head><body><p>회사 관련 뉴스가 없습니다.</p></body></html>",
                QUrl("about:blank")
            )
        else:
            # 상위 뉴스 기사를 텔레그램으로 전송
            self.send_top_articles_via_telegram(top_n=3)

    def show_selected_news_detail(self, current_index):
        """
        뉴스 리스트에서 항목 선택 시 해당 뉴스의 상세 정보를 HTML로 표시합니다.
        """
        if current_index < 0 or current_index >= len(self.articles):
            return

        article = self.articles[current_index]
        title = article['title']
        link = article['link']
        published = article['published']
        best_pdf = article['best_pdf']

        info_html = (
            f"<!DOCTYPE html>"
            f"<html><head><meta charset='UTF-8'></head><body>"
            f"<h2>제목: {title}</h2>"
            f"<p><strong>발행 일자:</strong> {published}</p>"
            f"<p><strong>복합 유사도:</strong> {article['similarity']:.2f}</p>"
            f"<p><strong>최고 기여 PDF:</strong> {best_pdf}</p>"
            f"</body></html>"
        )
        self.detail_view.setHtml(info_html, QUrl("about:blank"))
        self.detail_view.load(QUrl(link))

def main():
    """
    애플리케이션 실행 함수.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
