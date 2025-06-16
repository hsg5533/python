# PyQtTableWidget2.py
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TableWidgetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("TableWidget  예제")

        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(400, 300)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        students = {
            'no': ['2018001', '2018002', '2018003'],
            'name': ['홍길동', '이순신', '김성철'],
            'group': ['1학년', '2학년', '3학년']
        }
        column_idx_lookup = {'no': 0, 'name': 1, 'group': 2}
        
        column_headers = ['학번', '이름', '학년']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for k, v in students.items():
            col = column_idx_lookup[k]
            print(k,v,col)
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                if col == 2:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TableWidgetWindow()
    window.show()
    app.exec_()
