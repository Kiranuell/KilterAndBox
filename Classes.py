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


class ACCEPTDELETE(QWidget):
    def __init__(self, currentStuff, name):
        super().__init__()
        self.currentStuff = currentStuff
        self.stuffName = name
        self.initUI()

    def initUI(self):
        # создание окна
        self.setGeometry(300, 300, 165, 105)
        self.setWindowTitle('deleteStuff')

        self.text = QLabel(self)
        self.text.setText(f"Удалить {self.stuffName}?")
        self.text.move(15, 15)
        self.text.resize(100, 30)

        self.rejectButton = QPushButton(self)
        self.rejectButton.move(15, 60)
        self.rejectButton.resize(60, 30)
        self.rejectButton.setText("нет")
        self.rejectButton.clicked.connect(self.reject)

        # кнопка согласия
        self.acceptButton = QPushButton(self)
        self.acceptButton.move(90, 60)
        self.acceptButton.resize(60, 30)
        self.acceptButton.setText("да")
        self.acceptButton.clicked.connect(self.accept)

    def reject(self):
        self.close()

    def accept(self):
        cur.execute("DELETE FROM stuff WHERE ID == ?", (self.currentStuff,))
        con.commit()
        self.close()

class BOX(QWidget):
    def __init__(self, currentBox):
        super().__init__()
        self.initUI()
        self.currentBox = currentBox

    def initUI(self):
        # создание окна
        self.setGeometry(300, 300, 165, 105)
        self.setWindowTitle('remakeBox')

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
        cur.execute("""INSERT INTO stuff(name, isBox, inBox)
                          VALUES (?, 1, ?)""", (a, self.currentBox))
        con.commit()
        self.close()


class ITEM(QWidget):
    def __init__(self, currentBox, currentItem=None, data=["предмет", 1], edit=False):
        self.currentItem = currentItem
        self.currentBox = currentBox
        self.data = data
        self.edit = edit
        super().__init__()
        self.initUI()

    def initUI(self):
        # создание окна
        self.setGeometry(300, 300, 165, 105)
        self.setWindowTitle('remakeItem')

        # кнопка отказа
        self.rejectButton = QPushButton(self)
        self.rejectButton.move(15, 60)
        self.rejectButton.resize(60, 30)
        self.rejectButton.setText("нет")
        self.rejectButton.clicked.connect(self.reject)

        # кнопка согласия
        self.acceptButton = QPushButton(self)
        self.acceptButton.move(90, 60)
        self.acceptButton.resize(60, 30)
        self.acceptButton.setText("да")
        self.acceptButton.clicked.connect(self.accept)

        # поле названия предмета
        self.name = QLineEdit(self)
        self.name.move(15, 15)
        self.name.resize(80, 30)
        print(self.data[0])
        self.name.setText(str(self.data[0]))

        # поле количества предмета
        self.amount = QLineEdit(self)
        self.amount.move(110, 15)
        self.amount.resize(40, 30)
        self.amount.setText(str(self.data[1]))

        # значек "X"
        self.x = QLabel(self)
        self.x.setText("X")
        self.x.move(100, 15)
        self.x.resize(30, 30)

    def reject(self):
        self.close()

    def accept(self):
        if self.edit:
            name = self.name.text()
            amount = int(self.amount.text())
            currentItem = int(self.currentItem)
            cur.execute("""UPDATE stuff SET name = ?, amount = ? WHERE id = ?""", (name, amount, currentItem))
            con.commit()
            self.close()
        else:
            name = self.name.text()
            amount = int(self.amount.text())
            currentBox = self.currentBox
            cur.execute("""INSERT INTO stuff(name, amount, inBox) VALUES (?, ?, ?)""", (name, amount, currentBox))
            con.commit()
            self.close()
