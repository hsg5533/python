# PyQtWindowPushButton.py
import sys
from PyQt5.QtWidgets import *

class PushButtonWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("PushButtonWindow")

        btn = QPushButton("Click me", self)
        btn.move(20, 20)
        btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        QMessageBox.about(self, "메시지", "clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PushButtonWindow()
    window.show()
    app.exec_()
