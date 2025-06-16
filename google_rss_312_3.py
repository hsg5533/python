import os
if not os.path.exists("static"):
    os.makedirs("static")

import sys
import glob
import re
import time
import datetime
import requests
import feedparser        # RSS 피드 파싱용 라이브러리
import numpy as np       # 수치 계산용 라이브러리
import tensorflow as tf  # TensorFlow 라이브러리 (모델 로딩 및 연산)
import tensorflow_hub as hub  # TensorFlow Hub에서 모델 불러오기용 라이브러리
import fitz              # PyMuPDF: PDF 파일에서 텍스트 추출용

from urllib.parse import quote

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QListWidget, QSplitter, QProgressBar
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

        # 애플리케이션 실행 시 data/ 폴더 내의 PDF 파일을 자동으로 읽어옵니다.
        self.load_data_pdf_files()

    def load_data_pdf_files(self):
        """
        data/ 폴더 내의 모든 PDF 파일을 읽어와 임베딩 계산을 수행합니다.
        """
        data_folder = "data"
        file_paths = glob.glob(os.path.join(data_folder, "*.pdf"))
        if file_paths:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # 진행률 무한대
            self.worker = PDFEmbeddingWorker(file_paths, self.embed)
            self.worker.finished.connect(self.on_pdf_embeddings_finished)
            self.worker.start()
        else:
            print("data 폴더에 PDF 파일이 없습니다.")

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

    def fetch_news(self):
        """
        검색어 또는 PDF에서 추출한 회사명을 바탕으로 구글 뉴스 RSS를 검색합니다.
        GUI에는 전체 기사 목록을 표시하고, 텔레그램 전송 시에만 오늘 기준 전날 21시 ~ 오늘 오전 9시 사이의 기사만 전송합니다.
        """
        # 사용자가 검색어를 입력하지 않으면 PDF에서 추출한 회사명을 사용
        keyword = self.keyword_input.text().strip()
        if not keyword and self.pdf_data:
            keyword = extract_company_name(self.pdf_data[0]['text'])
            print("자동 추출 검색어:", keyword)
        if not keyword:
            print("검색어가 없습니다.")
            return

        sanitized_keyword = sanitize_keyword(keyword)
        region_info = self.region_combo.currentData()
        rss_url = f"https://news.google.com/rss/search?q={sanitized_keyword}&hl={region_info[0]}&gl={region_info[1]}&ceid={region_info[2]}"
        print("RSS URL:", rss_url)
        feed = feedparser.parse(rss_url)

        # GUI에 전체 기사 표시
        self.articles = []
        self.news_list.clear()
        for entry in feed.entries:
            article = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary,
                'published_parsed': entry.get('published_parsed', None)
            }
            self.articles.append(article)
            self.news_list.addItem(entry.title)

        # 텔레그램 전송 시에만 시간 필터 적용 (전날 21시 ~ 오늘 오전 9시)
        filtered_articles = []
        today_date = datetime.date.today()
        lower_bound = datetime.datetime.combine(today_date - datetime.timedelta(days=1), datetime.time(21, 0, 0))
        upper_bound = datetime.datetime.combine(today_date, datetime.time(9, 0, 0))
        for article in self.articles:
            pub_parsed = article.get('published_parsed')
            if pub_parsed:
                pub_date = datetime.datetime.fromtimestamp(time.mktime(pub_parsed))
                print(f"뉴스 발행 시간: {pub_date} (조건: {lower_bound} ~ {upper_bound})")
                if lower_bound <= pub_date <= upper_bound:
                    filtered_articles.append(article)
        if filtered_articles:
            self.send_top_articles_via_telegram(filtered_articles)
        else:
            print("텔레그램으로 전송할 조건에 맞는 뉴스 기사가 없습니다.")

    def show_selected_news_detail(self, index):
        """
        뉴스 리스트에서 선택된 항목의 상세 내용을 웹뷰에 표시합니다.
        여기서는 기사 원문 페이지를 QWebEngineView를 사용해 로드합니다.
        """
        if 0 <= index < len(self.articles):
            article = self.articles[index]
            self.detail_view.load(QUrl(article['link']))
        else:
            self.detail_view.setHtml("<html><body>뉴스 기사를 선택하세요.</body></html>")

    def send_top_articles_via_telegram(self, articles):
        """
        전달받은 뉴스 기사 리스트(필터링된 기사)를 텔레그램 메시지로 전송합니다.
        """
        if not articles:
            print("전송할 뉴스 기사가 없습니다.")
            return

        message_lines = ["<b>Filtered News Articles (전날 21시 ~ 오늘 오전 9시):</b>"]
        for idx, article in enumerate(articles, start=1):
            line = (f"{idx}. {article['title']}\n"
                    f"Link: {article['link']}")
            message_lines.append(line)
        message = "\n\n".join(message_lines)
        send_telegram_message(message, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

def main():
    """
    애플리케이션 실행 함수.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()