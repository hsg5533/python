import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from bs4 import BeautifulSoup

class DynamicCrawler(QWebEngineView):
    def __init__(self, url):
        super().__init__()
        # 자바스크립트 활성화 설정 (기존 브라우저 코드와 동일)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        # 페이지 로딩 완료 시점을 연결
        self.loadFinished.connect(self.on_load_finished)
        self.load(QUrl(url))
    
    def on_load_finished(self, ok):
        if ok:
            # 동적 콘텐츠가 모두 로드되도록 잠시(예: 1초) 대기 후 크롤링 진행
            QTimer.singleShot(1000, self.process_page)
        else:
            print("페이지 로드 실패")
            QApplication.instance().quit()
    
    def process_page(self):
        # 페이지의 최종 HTML을 가져옴
        self.page().toHtml(self.handle_html)
    
    def handle_html(self, html):
        # BeautifulSoup을 이용하여 HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')
        # 예시: 페이지 내 모든 링크(a 태그)를 추출하여 출력
        links = soup.find_all('img')
        print("추출된 링크들:")
        for link in links:
            href = link.get('src')
            if href:
                print(href)
        # 크롤링 후 프로그램 종료
        QApplication.instance().quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 크롤링할 URL (예시: 동적 콘텐츠가 있는 페이지)
    crawler = DynamicCrawler("https://www.naver.com")
    # 창을 띄우고 싶다면 show()를 사용 (필수는 아님)
    crawler.show()
    sys.exit(app.exec_())
