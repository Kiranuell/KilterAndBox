import sys
import sqlite3
from PyQt5.QtWidgets import *

con = sqlite3.connect("testbox.db")  # или :memory: чтобы сохранить в RAM
cur = con.cursor()
sizeBox = 50

class Kilter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.flag = True

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('KilterAndBox')

        self.butt = QPushButton(self)
        self.butt.resize(80, 80)
        self.butt.move(10, 10)
        self.butt.clicked.connect(self.click)

    def click(self):
        if self.flag:
            self.butt.move(50, 50)
        else:
            self.butt.move(10, 10)
        self.flag = not self.flag


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Kilter()
    ex.show()
    sys.exit(app.exec())