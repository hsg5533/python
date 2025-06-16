# PyQtWindowLineEdit.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CLineEditWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("ButtonLabelWindow")
        self.setGeometry(100,100,300,100)

        self.label = QLabel("이름 : ", self)
        self.label.move(20,20)
        self.label.resize(150,20)

        self.lineEdit = QLineEdit("", self)
        self.lineEdit.move(60,20)
        self.lineEdit.resize(200,20)
        self.lineEdit.textChanged.connect(self.lineEdit_textChanged)

        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        
        btnSave = QPushButton("저장", self)
        btnSave.move(10, 50)
        btnSave.clicked.connect(self.btnSave_clicked)

        btnClear = QPushButton("초기화", self)
        btnClear.move(100, 50)
        btnClear.clicked.connect(self.btnClear_clicked)

        btnQuit = QPushButton("닫기", self)
        btnQuit.move(190, 50)
        btnQuit.clicked.connect(self.btnQuit_clicked)
        #btnQuit.clicked.connect(QCoreApplication.instance().quit)  

    def btnSave_clicked(self):
        print(self.lineEdit.text())
        msg = "저장하시겠습니까?"
        msg += "\n이름 : " + self.lineEdit.text()
        buttonReply = QMessageBox.question(self, '저장', msg,
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                                           #QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)

        if buttonReply == QMessageBox.Yes:
            print('Yes clicked.')
            # 저장을 한다
            QMessageBox.about(self, "저장", "저장 되었습니다")
            self.statusBar.showMessage("저장 되었습니다")
        if buttonReply == QMessageBox.No:
            print('No clicked.')
        if buttonReply == QMessageBox.Cancel:
            print('Cancel')
            
    def btnClear_clicked(self):
        # 화면을 초기화 한다
        self.lineEdit.clear()

    def  btnQuit_clicked(self):
        # 프로그램을 종료한다
        sys.exit()

    def  lineEdit_textChanged(self):
        pass
        #self.statusBar.showMessage(self.lineEdit.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CLineEditWindow()
    window.show()
    app.exec_()
