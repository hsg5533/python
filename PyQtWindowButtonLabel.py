# PyQtWindowButtonLabel.py
import sys
from PyQt5.QtWidgets import *


class ButtonLabelWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("ButtonLabelWindow")
        self.setGeometry(100, 100, 300, 100)

        self.label = QLabel("Message : ", self)
        self.label.move(20, 20)
        self.label.resize(200, 20)

        btnSave = QPushButton("저장", self)
        btnSave.move(20, 50)
        btnSave.clicked.connect(self.btnSave_clicked)

        btnCancel = QPushButton("취소", self)
        btnCancel.move(120, 50)
        btnCancel.clicked.connect(self.btnCancel_clicked)

    def btnSave_clicked(self):
        self.label.setText("저장 되었습니다")

    def btnCancel_clicked(self):
        self.label.setText("취소 되었습니다")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ButtonLabelWindow()
    window.show()
    app.exec_()
