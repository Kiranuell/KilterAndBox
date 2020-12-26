import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import Qt, QtWidgets, QtCore

con = sqlite3.connect("testbox.db")
cur = con.cursor()


class PushButtonRight(QtWidgets.QPushButton):
    left_click = QtCore.pyqtSignal()
    right_click = QtCore.pyqtSignal()

    def __init__(self, string):
        super().__init__(string)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.left_click.emit()
        elif event.button() == Qt.Qt.RightButton:
            self.right_click.emit()

        QtWidgets.QPushButton.mousePressEvent(self, event)


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


class ACCEPTDELETE(QWidget):
    def __init__(self, currentStuff=0, name=0, isInTrash=0):
        super().__init__()
        self.currentStuff = currentStuff
        self.stuffName = name
        self.isInTrash = isInTrash
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
        if self.isInTrash:
            cur.execute("DELETE FROM stuff WHERE id == ?", (self.currentStuff,))
            con.commit()
            self.close()
        else:
            cur.execute("UPDATE stuff SET inBox = -1 WHERE ID == ?", (self.currentStuff,))
            con.commit()
            self.close()


class BOX(QWidget):
    def __init__(self, inBox, currentBox=None, name="коробка", edit=False):
        super().__init__()
        self.inBox = inBox
        self.currentBox = currentBox
        self.name = name
        self.edit = edit
        self.initUI()

    def initUI(self):
        # создание окна
        self.setGeometry(300, 300, 165, 105)
        self.setWindowTitle('remakeBox')

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
        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.move(15, 15)
        self.nameLineEdit.resize(135, 30)
        self.nameLineEdit.setText(self.name)

    def reject(self):
        self.close()

    def accept(self):
        name = self.nameLineEdit.text()
        if self.edit:
            cur.execute("""UPDATE stuff SET name = ? WHERE id = ?""", (name, self.currentBox))
            con.commit()
            self.close()
        else:
            cur.execute("""INSERT INTO stuff(name, isBox, inBox)
                                      VALUES (?, 1, ?)""", (name, self.inBox))
            con.commit()
            self.close()


class ITEM(QWidget):
    def __init__(self, currentBox, look, currentItem=None, data=["предмет", 1], edit=False):
        super().__init__()
        self.currentItem = currentItem
        self.currentBox = currentBox
        self.data = data
        self.edit = edit
        self.look = look
        self.initUI()

    def initUI(self):
        # создание окна
        self.setGeometry(300, 300, 165, 105)
        self.setWindowTitle('remakeItem')

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
        self.x.resize(15, 30)

        if self.look:
            self.name.setReadOnly(True)
            self.amount.setReadOnly(True)
            self.setGeometry(300, 300, 165, 65)
        else:
            self.rejectButton = QPushButton(self)
            self.rejectButton.move(15, 60)
            self.rejectButton.resize(60, 30)
            self.rejectButton.setText("нет")
            self.rejectButton.clicked.connect(self.reject)

            self.acceptButton = QPushButton(self)
            self.acceptButton.move(90, 60)
            self.acceptButton.resize(60, 30)
            self.acceptButton.setText("да")
            self.acceptButton.clicked.connect(self.accept)

    def reject(self):
        self.close()

    def accept(self):
        name = self.name.text()
        amount = int(self.amount.text())
        if self.edit:
            currentItem = int(self.currentItem)
            cur.execute("""UPDATE stuff SET name = ?, amount = ? WHERE id = ?""", (name, amount, currentItem))
            con.commit()
            self.close()
        else:
            currentBox = self.currentBox
            cur.execute("""INSERT INTO stuff(name, amount, inBox) VALUES (?, ?, ?)""", (name, amount, currentBox))
            con.commit()
            self.close()
