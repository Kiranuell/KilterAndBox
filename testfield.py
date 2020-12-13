import sys
import sqlite3
from PyQt5.QtWidgets import *
from Classes import split, join, BOX, ITEM

con = sqlite3.connect("testbox.db")
cur = con.cursor()
sizeBox = 50

class Kilter(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.initUI()
        self.upBox = []
        self.currentBox = None
        self.currentListStuff = []
        self.currentListName = []
        self.height = 500
        self.width = 500

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('KilterAndBox')
        self.drawStuff(None)

        self.returne = QPushButton(self)
        self.returne.move(15, 15)
        self.returne.resize(50, 30)
        self.returne.setText("назад")
        self.returne.setVisible(False)
        self.returne.clicked.connect(self.back)

    def drawStuff(self, box):
        for i in self.buttons:
            for j in i:
                if j:
                    j.deleteLater()
        stuff = cur.execute("SELECT id, isBox FROM stuff WHERE inBox IS ?", (box,))
        self.currentListStuff = []
        for i in stuff:
            self.currentListStuff.append(i)
        self.currentListName = []
        for i in self.currentListStuff:
            name = cur.execute("SELECT name FROM stuff WHERE id IS ?", (i[0],))
            for j in name:
                self.currentListName.append(*j)
        if self.currentListStuff:
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
                        self.buttons[i][j].setVisible(True)
                        if self.idTable[i][j][1]:
                            self.buttons[i][j].clicked.connect(self.clickBox)
                    x += 95
                y += 95
                x = 15
        else:
            self.buttons = []

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

    def clickBox(self):
        sender = self.sender()
        wi = (sender.pos().x() - 15) // 95
        hi = (sender.pos().y() - 60) // 95
        self.upBox.append(self.currentBox)
        self.currentBox = self.idTable[hi][wi][0]
        self.drawStuff(self.currentBox)
        self.drawUI()

    def back(self):
        self.currentBox = self.upBox[-1]
        self.upBox.pop()
        self.drawStuff(self.currentBox)
        self.drawUI()

    def drawUI(self):
        if self.upBox:
            self.returne.setVisible(True)
        else:
            self.returne.setVisible(False)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Kilter()
    ex.show()
    sys.exit(app.exec())
