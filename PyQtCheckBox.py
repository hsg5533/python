# PyQtCheckBox.py
import sys
from PyQt5.QtWidgets import *

class CheckBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("체크박스 예제")

        self.checkBox1 = QCheckBox("항목1", self)
        self.checkBox1.move(20, 20)
        self.checkBox1.setChecked(True)
        self.checkBox1.clicked.connect(self.checkBoxStateChanged)

        self.checkBox2 = QCheckBox("항목2", self)
        self.checkBox2.move(20, 40)
        self.checkBox2.clicked.connect(self.checkBoxStateChanged)

        self.checkBox3 = QCheckBox("항목3", self)
        self.checkBox3.move(20, 60)
        self.checkBox3.clicked.connect(self.checkBoxStateChanged)

    def checkBoxStateChanged(self):
        msg = ""
        if self.checkBox1.isChecked():
            msg += "항목1 "
        if self.checkBox2.isChecked():
            msg += "항목2 "
        if self.checkBox3.isChecked():
            msg += "항목3"
            
        QMessageBox.about(self, "선택된 항목", msg+ " 선택됨 ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckBoxWindow()
    window.show()
    app.exec_()
