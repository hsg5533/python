# PyQtGroupBox.py
import sys
from PyQt5.QtWidgets import *

class GroupBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("PushButtonWindow")

        groupBox = QGroupBox("항목 그룹", self)
        groupBox.move(10, 10)
        groupBox.resize(150, 80)

        self.radio1 = QRadioButton("항목1", self)
        self.radio1.move(20, 20)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.radioButton_clicked)

        self.radio2 = QRadioButton("항목2", self)
        self.radio2.move(20, 40)
        self.radio2.clicked.connect(self.radioButton_clicked)

        self.radio3 = QRadioButton("항목3", self)
        self.radio3.move(20, 60)
        self.radio3.clicked.connect(self.radioButton_clicked)

    def radioButton_clicked(self):
        msg = ""
        if self.radio1.isChecked():
            msg = "항목1"
        elif self.radio2.isChecked():
            msg = "항목2"
        else:
            msg = "항목3"
            
        QMessageBox.about(self, "선택된 항목", msg+ " 선택됨 ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GroupBoxWindow()
    window.show()
    app.exec_()
