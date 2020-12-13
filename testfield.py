import sys
import sqlite3
from PyQt5.QtWidgets import *
from Classes import split, join

con = sqlite3.connect("testbox.db")  # или :memory: чтобы сохранить в RAM
cur = con.cursor()
sizeBox = 50

class Kilter(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.initUI()
        self.upBox = None
        self.currentBox = None
        self.currentListStuff = []
        self.currentListName = []
        self.height = 200
        self.width = 500

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('KilterAndBox')
        self.drawStuff(None)

    def drawStuff(self, box):
        for i in self.buttons:
            for j in i:
                if j:
                    j.deleteLater()
        stuff = cur.execute("SELECT id FROM stuff WHERE inBox IS ?", (box,))
        self.currentListStuff = []
        for i in stuff:
            self.currentListStuff.append(*i)
        self.currentListName = []
        for i in self.currentListStuff:
            name = cur.execute("SELECT name FROM stuff WHERE id IS ?", (i,))
            for j in name:
                self.currentListName.append(*j)
        self.widthItem = (self.size().width() - 15) // 95
        if self.widthItem > len(self.currentListStuff):
            self.widthItem = len(self.currentListStuff)
        self.highItem = int((len(self.currentListStuff) / self.widthItem) + 0.99999)
        self.idTable = split(self.currentListStuff, self.widthItem)
        self.nameTable = split(self.currentListName, self.widthItem)
        print(self.widthItem, self.highItem)
        x = 15
        y = 60
        self.buttons = [[None] * self.widthItem for _ in range(self.highItem)]
        print(self.nameTable)
        for i in range(self.highItem):
            for j in range(self.widthItem):
                if self.nameTable[i][j] != 0:
                    self.buttons[i][j] = QPushButton(self)
                    self.buttons[i][j].resize(80, 80)
                    self.buttons[i][j].move(x, y)
                    self.buttons[i][j].setText(str(self.nameTable[i][j]))
                x += 95
            y += 95
            x = 15

    def moveStuff(self):
        self.buttons = join(self.buttons)
        self.widthItem = (self.size().width() - 15) // 95
        if self.widthItem > len(self.buttons):
            self.widthItem = len(self.buttons)
        self.highItem = int((len(self.buttons) / self.widthItem) + 0.9999)
        self.buttons = split(self.buttons, self.widthItem)
        print(self.highItem, self.widthItem, self.buttons)
        x = 15
        y = 60
        for i in range(self.highItem):
            for j in range(self.widthItem):
                if self.buttons[i][j] != 0:
                    self.buttons[i][j].move(x, y)
                    x += 95
            y += 95
            x = 15




    def resizeEvent(self, event):
        self.width = self.size().width()
        self.moveStuff()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Kilter()
    ex.show()
    sys.exit(app.exec())
