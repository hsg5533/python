import os
if not os.path.exists("static"):
    os.makedirs("static")

import sys
import feedparser        # RSS 피드 파싱용 라이브러리
import numpy as np       # 수치 계산용 라이브러리
import tensorflow as tf  # TensorFlow 라이브러리 (모델 로딩 및 연산)
import tensorflow_hub as hub  # TensorFlow Hub에서 모델 불러오기용 라이브러리
import fitz              # PyMuPDF: PDF 파일에서 텍스트 추출용
import re
import requests          # 텔레그램 API 호출용
import datetime          # 날짜 및 시간 처리용
import time              # 타임존 변환용

from urllib.parse import quote

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QListWidget, QSplitter, QFileDialog, QProgressBar
)
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView  # 웹 페이지 렌더링 위젯

# 텔레그램 봇 정보 (실제 값으로 변경)
TELEGRAM_BOT_TOKEN = "7763945499:AAHBg1GbFHL6GUYq5NW_2bbXo4QbpGKxtKU"
TELEGRAM_CHAT_ID = "7588489578"

def load_pdf_text(pdf_path):
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
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def extract_company_name(text):
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
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, data=payload)
    print("텔레그램 전송 응답:", response.json())
    return response.json()

def sanitize_keyword(keyword):
    sanitized_keyword = re.sub(r'[\r\n]+', ' ', keyword).strip()
    return quote(sanitized_keyword)

class PDFEmbeddingWorker(QThread):
    finished = pyqtSignal(list)

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
                    for i, sentence in enumerate(sentences):
                        emb_vector = sentence_embeddings[i].numpy() if hasattr(sentence_embeddings[i], "numpy") else sentence_embeddings[i]
                        print(f"문장 {i+1}: {sentence}")
                        print(f"임베딩: {emb_vector[:5]} ...\n")
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

        print("TensorFlow Hub 모델 로딩 중...")
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        print("모델 로드 완료.")
        self.pdf_data = []

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

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

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        top_layout = QHBoxLayout()
        self.keyword_label = QLabel("검색어 (미입력시 자동 검색):")
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("예: 테슬라, 아이폰 ... (비워두면 PDF에서 추출)")
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
        file_paths, _ = QFileDialog.getOpenFileNames(self, "PDF 파일 선택", "", "PDF Files (*.pdf)")
        if file_paths:
            self.company_file_line.setText("; ".join(file_paths))
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            self.worker = PDFEmbeddingWorker(file_paths, self.embed)
            self.worker.finished.connect(self.on_pdf_embeddings_finished)
            self.worker.start()

    def on_pdf_embeddings_finished(self, pdf_data):
        self.pdf_data = pdf_data
        self.progress_bar.setVisible(False)
        if self.pdf_data:
            print("모든 PDF 파일 업로드 및 임베딩 업데이트 완료.")
        else:
            print("선택한 PDF들에서 텍스트 추출 실패.")

    def compute_composite_similarity(self, news_embedding):
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
        encoded_keyword = sanitize_keyword(keyword)
        base_url = "https://news.google.com/rss/search"
        return f"{base_url}?q={encoded_keyword}&hl={hl}&gl={gl}&ceid={ceid}"

    def send_top_articles_via_telegram(self):
        """
        검색 결과에서 모든 뉴스를 텔레그램 메시지로 전송합니다.
        """
        if not self.articles:
            print("발송할 뉴스 기사가 없습니다.")
            return

        # 유사도 기준 내림차순 정렬 후, 모든 기사 사용
        sorted_articles = sorted(self.articles, key=lambda x: x['similarity'], reverse=True)
        message_lines = ["<b>All Similar News Articles:</b>"]
        for idx, article in enumerate(sorted_articles, start=1):
            line = (f"{idx}. {article['title']} (sim={article['similarity']:.2f})\n"
                f"Link: {article['link']}")
            message_lines.append(line)
        message = "\n\n".join(message_lines)
        send_telegram_message(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    def fetch_news(self):
        """
        오늘 기준 전날 21시부터 오늘 08시 59분 59초까지 출판된 뉴스만 처리합니다.
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
        print("검색된 피드의 길이", len(feed.entries))
        if not feed.entries:
            self.news_list.clear()
            self.detail_view.setHtml(
                "<html><head><meta charset='UTF-8'></head><body><p>검색 결과가 없습니다.</p></body></html>",
                QUrl("about:blank")
            )
            return

        # 오늘 기준 전날 21시 ~ 오늘 08시 59분 59초 (로컬 시간 기준)
        today_date = datetime.date.today()
        lower_bound = datetime.datetime.combine(today_date - datetime.timedelta(days=1), datetime.time(21, 0, 0))
        upper_bound = datetime.datetime.combine(today_date, datetime.time(8, 59, 59))

        self.news_list.clear()
        self.articles = []
        similarity_threshold = 0.2

        for entry in feed.entries:
            if hasattr(entry, 'published_parsed'):
                pub = entry.published_parsed
                # published_parsed를 로컬 시간(datetime)으로 변환
                pub_date = datetime.datetime.fromtimestamp(time.mktime(pub))
                # 디버그 출력: 각 뉴스의 발행 시간을 확인해보세요.
                print(f"뉴스 발행 시간: {pub_date} (조건: {lower_bound} ~ {upper_bound})")
                if not (lower_bound <= pub_date <= upper_bound):
                    continue
            else:
                continue

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
            self.send_top_articles_via_telegram()

    def show_selected_news_detail(self, current_index):
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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
