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

        self.backButton = QPushButton(self)
        self.backButton.move(15, 15)
        self.backButton.resize(50, 30)
        self.backButton.setText("назад")
        self.backButton.setVisible(False)
        self.backButton.clicked.connect(self.back)

        self.addBoxButton = QPushButton(self)
        self.addBoxButton.move(15, 15)
        self.addBoxButton.resize(80, 30)
        self.addBoxButton.setText("нов.коробка")
        self.addBoxButton.clicked.connect(self.addBox)

        self.addItemButton = QPushButton(self)
        self.addItemButton.move(100, 15)
        self.addItemButton.resize(80, 30)
        self.addItemButton.setText("нов.предмет")
        self.addItemButton.clicked.connect(self.addItem)

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
            self.backButton.setVisible(True)
            self.addBoxButton.move(70, 15)
            self.addItemButton.move(155, 15)
        else:
            self.backButton.setVisible(False)
            self.addBoxButton.move(15, 15)
            self.addItemButton.move(100, 15)

    def addBox(self):
        self.addbox = BOX(self.currentBox)
        self.addbox.show()

    def addItem(self):
        self.additem = ITEM(self.currentBox)
        self.additem.show()







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Kilter()
    ex.show()
    sys.exit(app.exec())
