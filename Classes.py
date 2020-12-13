import sys
import sqlite3
from PyQt5.QtWidgets import *

con = sqlite3.connect("testbox.db")
cur = con.cursor()

def split(arr, size):
    arrs = []
    if len(arr) <= size:
        return [arr]
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    while len(arrs[-1]) < size:
        arrs[-1].append(0)
    return arrs

def join(arr):
    arrs = []
    for i in arr:
        for j in i:
            if j:
                arrs.append(j)
    return arrs

class BOX(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # создание окна
        self.setGeometry(300, 300, 165, 105)
        self.setWindowTitle('NameItem')

        # кнопка отказа
        self.no = QPushButton(self)
        self.no.move(15, 60)
        self.no.resize(60, 30)
        self.no.setText("нет")
        self.no.clicked.connect(self.reject)

        # кнопка согласия
        self.yes = QPushButton(self)
        self.yes.move(90, 60)
        self.yes.resize(60, 30)
        self.yes.setText("да")
        self.yes.clicked.connect(self.accept)

        # поле названия коробки
        self.name = QLineEdit(self)
        self.name.move(15, 15)
        self.name.resize(135, 30)
        self.name.setText("коробка")

    def reject(self):
        self.close()

    def accept(self):
        a = self.name.text()
        cur.execute("""INSERT INTO box(name)
                          VALUES (?)""", (a,))
        con.commit()
        self.close()

class ITEM(QWidget):
    def __init__(self, nowbox, data=["предмет", 1], edit = False):
        self.nowbox = nowbox
        self.data = data
        self.edit = edit
        super().__init__()
        self.initUI()


    def initUI(self):
        # создание окна
        self.setGeometry(300, 300, 165, 105)
        self.setWindowTitle('NameItem')

        # кнопка отказа
        self.no = QPushButton(self)
        self.no.move(15, 60)
        self.no.resize(60, 30)
        self.no.setText("нет")
        self.no.clicked.connect(self.reject)

        # кнопка согласия
        self.yes = QPushButton(self)
        self.yes.move(90, 60)
        self.yes.resize(60, 30)
        self.yes.setText("да")
        self.yes.clicked.connect(self.accept)

        # поле названия предмета
        self.name = QLineEdit(self)
        self.name.move(15, 15)
        self.name.resize(80, 30)
        print(self.data[0])
        self.name.setText(str(self.data[0]))

        # поле количества предмета
        self.amou = QLineEdit(self)
        self.amou.move(110, 15)
        self.amou.resize(40, 30)
        self.amou.setText(str(self.data[1]))

        # значек "X"
        self.x = QLabel(self)
        self.x.setText("X")
        self.x.move(100, 15)
        self.x.resize(30, 30)

    def reject(self):
        self.close()

    def accept(self):
        if self.edit:
            a = self.name.text()
            b = int(self.amou.text())
            c = int(self.nowbox)
            cur.execute("""UPDATE item
                           SET name = ?
                           WHERE id = ?""", (a, c))
            cur.execute("""UPDATE item
                           SET amount = ?
                           WHERE id = ?""", (b, c))
            con.commit()
            self.close()
        else:
            a = self.name.text()
            b = int(self.amou.text())
            c = int(self.nowbox)
            cur.execute("""INSERT INTO item(NAME, AMOUNT, BOX)
                              VALUES (?, ?, ?)""", (a, b, c))
            con.commit()
            self.close()