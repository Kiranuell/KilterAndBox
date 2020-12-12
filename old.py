import sys
import sqlite3
from PyQt5.QtWidgets import *

con = sqlite3.connect("testbox.db") # или :memory: чтобы сохранить в RAM
cur = con.cursor()

stop = False

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

class ITOG(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # создание окна
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('KilterBox')

        # кнопка создания коробки
        self.newBox = QPushButton(self)
        self.newBox.move(15, 15)
        self.newBox.resize(80, 30)
        self.newBox.setText("нов.коробка")
        self.newBox.clicked.connect(self.addBox)

        # переключение режима удаления
        self.delete = QRadioButton(self)
        self.delete.move(110, 15)
        self.delete.setText("удалить")
        self.delete.resize(70, 30)

        # поле поиска предмета или коробки
        self.findBox = QLineEdit(self)
        self.findBox.move(195, 15)
        self.findBox.resize(self.size().width() - 210, 30)
        self.findBox.setText("Найти коробку или предмет")


        # кнопка создания предмета
        self.newItem = QPushButton(self)
        self.newItem.move(80, 15)
        self.newItem.resize(80, 30)
        self.newItem.setText("нов.предмет")
        self.newItem.setVisible(False)
        self.newItem.clicked.connect(self.addItem)

        # поиск предмета
        self.findItem = QLineEdit(self)
        self.findItem.move(260, 15)
        self.findItem.resize(self.size().width() - 275, 30)
        self.findItem.setText("Найти предмет")
        self.findItem.setVisible(False)

        # создание кнопок коробок
        self.boxUpdate()

        # кнопка возвращения
        self.returne = QPushButton(self)
        self.returne.move(15, 15)
        self.returne.resize(50, 30)
        self.returne.setText("назад")
        self.returne.setVisible(False)
        self.returne.clicked.connect(self.back)

        # кнопки предметов

    def clickbox(self):
        if self.delete.isChecked():
            cur.execute("DELETE FROM box WHERE ID == ?", (self.nowbutt,))
            con.commit()
        else:
            self.setWindowTitle(self.names[self.nowbutt])
            self.returne.setVisible(True)
            self.newItem.setVisible(True)
            self.findItem.setVisible(True)
            self.newBox.setVisible(False)
            self.findBox.setVisible(False)
            self.delete.move(175, 15)
            for i in range(self.hi):
                for j in range(self.wi):
                    if self.buttons[i][j] != None:
                        self.buttons[i][j].setVisible(False)
            self.itemUpdate()

    def back(self):
        self.setWindowTitle('KilterBox')
        self.returne.setVisible(False)
        self.newItem.setVisible(False)
        self.findItem.setVisible(False)
        self.newBox.setVisible(True)
        self.findBox.setVisible(True)
        self.delete.move(110, 15)
        self.boxUpdate()
        for i in range(self.hi):
            for j in range(self.wi):
                if self.buttons[i][j] != None:
                    self.buttons[i][j].setVisible(True)
        for i in range(self.hiI):
            for j in range(self.wiI):
                if self.items[i][j] != None:
                    self.items[i][j].setVisible(False)

    def itemClicked(self):
        sender = self.sender()
        wi = sender.pos().x() - 15
        if wi != 0:
            wi = wi // 95
        hi = sender.pos().y() - 60
        if hi != 0:
            hi = hi // 95
        self.nowIt = int(self.getitmes[hi][wi])

    def clickitem(self):
        self.additem = ITEM(self.nowbutt, (self.namesI[self.nowIt]), True)
        self.additem.show()

    def addBox(self):
        self.addbox = BOX()
        self.addbox.show()

    def addItem(self):
        self.additem = ITEM(self.nowbutt)
        self.additem.show()

    def resizeEvent(self, event):
        self.findBox.resize(self.size().width() - 210, 30)
        self.findItem.resize(self.size().width() - 275, 30)

    def boxUpdate(self):
        # кнопки коробок
        boxs = cur.execute("SELECT ID FROM box")
        self.case = []
        for i in boxs:
            self.case.append(i[0])
        self.names = {}
        for i in self.case:
            self.name = cur.execute("SELECT name FROM box WHERE ID == ?", (i,))
            for j in self.name:
                self.names[i] = j[0]
        self.wi = (self.size().width() - 15) // 95
        self.hi = len(self.case) / self.wi
        if self.hi % 1 != 0:
            self.hi = int(self.hi) + 1
        else:
            self.hi = int(self.hi)
        self.getbuttons = split(self.case, self.wi)
        x = 15
        y = 60
        self.buttons = [[None] * self.wi for _ in range(self.hi)]
        for i in range(self.hi):
            for j in range(self.wi):
                if self.getbuttons[i][j] != 0:
                    self.buttons[i][j] = QPushButton(self)
                    self.buttons[i][j].resize(80, 80)
                    self.buttons[i][j].move(x, y)
                    self.buttons[i][j].clicked.connect(self.boxClicked)
                    self.buttons[i][j].clicked.connect(self.clickbox)
                    self.buttons[i][j].setText(self.names[self.getbuttons[i][j]])
                    x += 95
            y += 95
            x = 15
        self.show()

    def itemUpdate(self):
        # кнопки предметов
        items = cur.execute("SELECT id FROM item WHERE box == ?", (self.nowbutt, ))
        self.stack = []
        for i in items:
            self.stack.append(i[0])
        self.namesI = {}
        for i in self.stack:
            self.nameI = cur.execute("SELECT name FROM item WHERE id == ?", (i,))
            for j in self.nameI:
                self.namesI[i] = [j[0]]
            self.amoun = cur.execute("SELECT amount FROM item WHERE id == ?", (i,))
            for d in self.amoun:
                self.namesI[i].append(d[0])
        self.wiI = (self.size().width() - 15) // 95
        self.getitmes = split(self.stack, self.wiI)
        self.wiI = len(self.getitmes[0])
        self.hiI = len(self.getitmes)
        x = 15
        y = 60
        self.items = [[None] * self.wiI for _ in range(self.hiI)]
        for i in range(self.hiI):
            for j in range(self.wiI):
                if self.getitmes[i][j] != 0:
                    self.items[i][j] = QPushButton(self)
                    self.items[i][j].resize(80, 80)
                    self.items[i][j].move(x, y)
                    self.items[i][j].clicked.connect(self.itemClicked)
                    self.items[i][j].clicked.connect(self.clickitem)
                    self.items[i][j].setText(self.namesI[self.getitmes[i][j]][0])
                    self.items[i][j].setVisible(True)
                    x += 95
            y += 95
            x = 15
        self.show()


    def boxClicked(self):
        sender = self.sender()
        wi = sender.pos().x() - 15
        if wi != 0:
            wi = wi // 95
        hi = sender.pos().y() - 60
        if hi != 0:
            hi = hi // 95
        self.nowbutt = int(self.getbuttons[hi][wi])


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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ITOG()
    ex.show()
    sys.exit(app.exec())