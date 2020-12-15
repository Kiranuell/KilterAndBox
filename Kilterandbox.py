import sys
import sqlite3
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from Classes import split, join, BOX, ITEM, ACCEPTDELETE

con = sqlite3.connect("testbox.db")
cur = con.cursor()

class Kilter(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.upBox = []
        self.currentBox = None
        self.currentListStuff = []
        self.height = 500
        self.width = 500

        oImage = QImage("BoxTexture.jpg")
        sImage = oImage.scaled(QSize(300, 200))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.initUI()

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
        self.backButton.setStyleSheet('background: rgb(255, 171, 0);')

        self.addBoxButton = QPushButton(self)
        self.addBoxButton.move(15, 15)
        self.addBoxButton.resize(80, 30)
        self.addBoxButton.setText("нов.коробка")
        self.addBoxButton.clicked.connect(self.addBox)
        self.addBoxButton.setStyleSheet('background: rgb(255, 171, 0);')

        self.addItemButton = QPushButton(self)
        self.addItemButton.move(100, 15)
        self.addItemButton.resize(80, 30)
        self.addItemButton.setText("нов.предмет")
        self.addItemButton.clicked.connect(self.addItem)
        self.addItemButton.setStyleSheet('background: rgb(255, 171, 0);')

        self.deleteRadioButton = QRadioButton(self)
        self.deleteRadioButton.move(190, 15)
        self.deleteRadioButton.setText("удалить")
        self.deleteRadioButton.resize(70, 30)

    def drawStuff(self, box):
        for i in self.buttons:
            for j in i:
                if j:
                    j.deleteLater()
        if self.windowTitle() == "мусорка":
            boxId = cur.execute("SELECT id FROM stuff WHERE isBox IS 1")
            boxExist = []
            for i in boxId:
                boxExist.append(*i)
            trashStuff = cur.execute(f"SELECT id, name, isBox FROM stuff WHERE inBox NOT IN ({(', ').join(list(map(str, boxExist)))})")
            self.trashList = []
            for i in trashStuff:
                self.trashList.append(i)
            if self.trashList:
                self.widthItem = (self.size().width() - 15) // 95
                if self.widthItem > len(self.trashList):
                    self.widthItem = len(self.trashList)
                self.highItem = int((len(self.trashList) / self.widthItem) + 0.99999)
                self.idTable = split(self.trashList, self.widthItem)
                x = 15
                y = 60
                self.buttons = [[None] * self.widthItem for _ in range(self.highItem)]
                for i in range(self.highItem):
                    for j in range(self.widthItem):
                        if self.idTable[i][j] != 0:
                            self.buttons[i][j] = QPushButton(self)
                            self.buttons[i][j].resize(80, 80)
                            self.buttons[i][j].move(x, y)
                            self.buttons[i][j].setText(str(self.idTable[i][j][1]))
                            self.buttons[i][j].setVisible(True)
                            if self.idTable[i][j][2]:
                                self.buttons[i][j].clicked.connect(self.clickBox)
                                self.buttons[i][j].setStyleSheet('background: rgb(255, 171, 0);')
                            else:
                                self.buttons[i][j].setStyleSheet('background: rgb(255, 215, 0);')
                        x += 95
                    y += 95
                    x = 15
            else:
                self.buttons = []

        else:
            stuff = cur.execute("SELECT id, name, isBox FROM stuff WHERE inBox IS ?", (box,))
            self.currentListStuff = []
            for i in stuff:
                self.currentListStuff.append(i)
            if not self.upBox:
                self.currentListStuff.append([None, "мусорка", 1])
            if self.currentListStuff:
                self.widthItem = (self.size().width() - 15) // 95
                if self.widthItem > len(self.currentListStuff):
                    self.widthItem = len(self.currentListStuff)
                self.highItem = int((len(self.currentListStuff) / self.widthItem) + 0.99999)
                self.idTable = split(self.currentListStuff, self.widthItem)
                x = 15
                y = 60
                self.buttons = [[None] * self.widthItem for _ in range(self.highItem)]
                for i in range(self.highItem):
                    for j in range(self.widthItem):
                        if self.idTable[i][j] != 0:
                            self.buttons[i][j] = QPushButton(self)
                            self.buttons[i][j].resize(80, 80)
                            self.buttons[i][j].move(x, y)
                            self.buttons[i][j].setText(str(self.idTable[i][j][1]))
                            self.buttons[i][j].setVisible(True)
                            if self.idTable[i][j][0] == None and self.idTable[i][j][1] == "мусорка":
                                self.buttons[i][j].clicked.connect(self.clickBox)
                                self.buttons[i][j].setStyleSheet('background: rgb(168, 168, 168);')
                            elif self.idTable[i][j][2]:
                                self.buttons[i][j].clicked.connect(self.clickBox)
                                self.buttons[i][j].setStyleSheet('background: rgb(255, 171, 0);')
                            else:
                                self.buttons[i][j].setStyleSheet('background: rgb(255, 215, 0);')
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
        if self.deleteRadioButton.isChecked():
            self.deleteStuff = ACCEPTDELETE(self.idTable[hi][wi][0], self.idTable[hi][wi][1])
            self.deleteStuff.show()
        else:
            self.upBox.append([self.currentBox, self.windowTitle()])
            self.setWindowTitle(self.idTable[hi][wi][1])
            self.currentBox = self.idTable[hi][wi][0]
            self.drawUI()
            self.drawStuff(self.currentBox)

    def back(self):
        self.setWindowTitle(self.upBox[-1][1])
        self.currentBox = self.upBox[-1][0]
        self.upBox.pop()
        self.drawStuff(self.currentBox)
        self.drawUI()

    def drawUI(self):
        if self.upBox:
            self.backButton.setVisible(True)
            self.addBoxButton.move(70, 15)
            self.addItemButton.move(155, 15)
            self.deleteRadioButton.move(245, 15)
        else:
            self.backButton.setVisible(False)
            self.addBoxButton.move(15, 15)
            self.addItemButton.move(100, 15)
            self.deleteRadioButton.move(190, 15)

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
