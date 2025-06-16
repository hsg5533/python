# PyQtTableWidget.py
import sys
from PyQt5.QtWidgets import *

class TableWidgetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("TableWidget  예제")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(400, 300)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem("(0,0)"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("(0,1)"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("(1,0)"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("(1,1)"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableWidgetWindow()
    window.show()
    app.exec_()
