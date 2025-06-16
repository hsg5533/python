# PyQtSpinBox.py
import sys
from PyQt5.QtWidgets import *

class SpinBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("스핀박스  예제")

        label = QLabel("수량: ", self)
        label.move(10, 20)
        
        self.spinBox = QSpinBox(self)
        self.spinBox.move(40, 20)
        self.spinBox.resize(60, 20)
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)

    def spinBoxValueChanged(self):
        val = self.spinBox.value()
        print(val)
        msg = "선택된 값: %s" %val
        print(msg)
        QMessageBox.about(self, "선택된 값", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpinBoxWindow()
    window.show()
    app.exec_()
