import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings, QWebEnginePage

# QWebEnginePage를 상속받아 링크 클릭 시 같은 창에서 페이지를 로드하도록 오버라이드
class MyWebEnginePage(QWebEnginePage):
    def acceptNavigationRequest(self, url, nav_type, isMainFrame):
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            self.view().setUrl(url)
            return False  # 기본 동작 방지
        return super().acceptNavigationRequest(url, nav_type, isMainFrame)

    # 새 창 요청을 처리할 때 새 QWebEnginePage를 생성하고, URL 변경 시 현재 뷰로 로드
    def createWindow(self, _type):
        new_page = QWebEnginePage(self)  # 새로운 QWebEnginePage 생성
        new_page.urlChanged.connect(lambda url: self.view().setUrl(url))
        return new_page

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # QWebEngineView 객체 생성 및 초기 URL 설정
        self.browser = QWebEngineView()
        # 커스텀 페이지로 교체
        self.browser.setPage(MyWebEnginePage(self.browser))
        self.browser.setUrl(QUrl("http://www.google.com"))
        
        # 자바스크립트 활성화 설정
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # 도구 모음 생성
        navbar = QToolBar()
        self.addToolBar(navbar)

        # 뒤로가기 버튼
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # 앞으로가기 버튼
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # 새로고침 버튼
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # URL 입력창 추가
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # URL 변경 시 주소창 업데이트
        self.browser.urlChanged.connect(self.update_url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("My Browser")
    window = MainWindow()
    sys.exit(app.exec_())