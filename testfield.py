import sys
import sqlite3
from PyQt5 import Qt

from PyQt5 import Qt, QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import *
from Classes import split, join, BOX, ITEM, ACCEPTDELETE, PushButtonRight
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import  QSize, QRect
from PyQt5 import QtWidgets, uic

con = sqlite3.connect("testbox.db")
cur = con.cursor()

distanceBetweenButtons = 10
buttonsHeight = 30
buttonsWidth = 80

con = sqlite3.connect("testbox.db")
cur = con.cursor()

class KilterAndBox(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.upBox = []
        self.currentBox = None
        self.currentListStuff = []
        self.idTable = []
        oImage = QImage("BoxTexture.jpg")
        sImage = oImage.scaled(QSize(300, 200))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('KilterAndBox')

        self.fullBackButton = QPushButton(self)
        self.fullBackButton.setVisible(False)
        self.fullBackButton.move(distanceBetweenButtons, distanceBetweenButtons)
        self.fullBackButton.resize(buttonsWidth, buttonsHeight)
        self.fullBackButton.setText("на главную")
        self.fullBackButton.clicked.connect(self.fullBack)
        self.fullBackButton.setStyleSheet('background: rgb(245, 222, 179);') # предмет
        self.fullBackButton.setStyleSheet('background: rgb(229, 184, 135);') # кнопка или коробка

        self.backButton = QPushButton(self)
        self.backButton.setVisible(False)
        self.backButton.move(distanceBetweenButtons, buttonsHeight + distanceBetweenButtons * 2)
        self.backButton.resize(buttonsWidth, buttonsHeight)
        self.backButton.setText("назад")
        self.backButton.clicked.connect(self.back)
        self.backButton.setStyleSheet('background: rgb(229, 184, 135);')

        self.addBoxButton = QPushButton(self)
        self.addBoxButton.move(distanceBetweenButtons, distanceBetweenButtons)
        self.addBoxButton.resize(buttonsWidth, buttonsHeight)
        self.addBoxButton.setText("нов.коробка")
        self.addBoxButton.clicked.connect(self.addBox)
        self.addBoxButton.setStyleSheet('background: rgb(229, 184, 135);')

        self.addItemButton = QPushButton(self)
        self.addItemButton.move(distanceBetweenButtons, buttonsHeight + distanceBetweenButtons * 2)
        self.addItemButton.resize(buttonsWidth, buttonsHeight)
        self.addItemButton.setText("нов.предмет")
        self.addItemButton.clicked.connect(self.addItem)
        self.addItemButton.setStyleSheet('background: rgb(229, 184, 135);')

        self.openRadioButton = QRadioButton(self)
        self.openRadioButton.move(buttonsWidth * 1 + distanceBetweenButtons * 2, distanceBetweenButtons)
        self.openRadioButton.resize(buttonsWidth, buttonsHeight)
        self.openRadioButton.setText("открыть")

        self.deleteRadioButton = QRadioButton(self)
        self.deleteRadioButton.move(buttonsWidth * 1 + distanceBetweenButtons * 2,
                                    buttonsHeight + distanceBetweenButtons * 2)
        self.deleteRadioButton.resize(buttonsWidth, buttonsHeight)
        self.deleteRadioButton.setText("удалить")

        self.singleSelectionRadioButton = QRadioButton(self)
        self.singleSelectionRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3, distanceBetweenButtons)
        self.singleSelectionRadioButton.resize(buttonsWidth, buttonsHeight)
        self.singleSelectionRadioButton.setText("единица")

        self.multipleSelectionRadioButton = QRadioButton(self)
        self.multipleSelectionRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3,
                                    buttonsHeight + distanceBetweenButtons * 2)
        self.multipleSelectionRadioButton.resize(buttonsWidth, buttonsHeight)
        self.multipleSelectionRadioButton.setText("множество")

        self.executeRadioButton = QRadioButton(self)
        self.executeRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4, distanceBetweenButtons)
        self.executeRadioButton.resize(buttonsWidth, buttonsHeight)
        self.executeRadioButton.setText("выполнить")

        self.planRadioButton = QRadioButton(self)
        self.planRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4,
                                    buttonsHeight + distanceBetweenButtons * 2)
        self.planRadioButton.resize(buttonsWidth, buttonsHeight)
        self.planRadioButton.setText("записать")

        self.openDeleteButtonGroup = QButtonGroup()
        self.openDeleteButtonGroup.addButton(self.openRadioButton)
        self.openDeleteButtonGroup.addButton(self.deleteRadioButton)
        self.openRadioButton.toggle()

        self.singleMultipleButtonGroup = QButtonGroup()
        self.singleMultipleButtonGroup.addButton(self.singleSelectionRadioButton)
        self.singleMultipleButtonGroup.addButton(self.multipleSelectionRadioButton)
        self.singleSelectionRadioButton.toggle()

        self.executePlanDeleteButtonGroup = QButtonGroup()
        self.executePlanDeleteButtonGroup.addButton(self.executeRadioButton)
        self.executePlanDeleteButtonGroup.addButton(self.planRadioButton)
        self.executeRadioButton.toggle()

        self.findButton = QPushButton(self)
        self.findButton.move(distanceBetweenButtons, buttonsHeight * 2 + distanceBetweenButtons * 3)
        self.findButton.resize(buttonsWidth, buttonsHeight)
        self.findButton.setText("найти")
        self.findButton.setStyleSheet('background: rgb(240, 240, 240);;')

        self.findLineEdit = QLineEdit(self)
        self.findLineEdit.move(buttonsWidth * 1 + distanceBetweenButtons * 2,
                               buttonsHeight * 2 + distanceBetweenButtons * 3)
        self.findLineEdit.resize(self.size().width() - (buttonsWidth * 1 + distanceBetweenButtons * 3), buttonsHeight)
        self.findLineEdit.setStyleSheet('background: rgb(240, 240, 240);;')

        self.noteButton = QPushButton(self)
        self.noteButton.move(distanceBetweenButtons, self.size().height() - (distanceBetweenButtons + buttonsHeight))
        self.noteButton.resize(self.size().width() - distanceBetweenButtons * 2, buttonsHeight)
        self.noteButton.setText("заметки")
        self.noteButton.setStyleSheet('background: rgb(229, 184, 135);;')





    def resizeEvent(self, event):
        self.findLineEdit.resize(self.size().width() - (buttonsWidth * 1 + distanceBetweenButtons * 3), buttonsHeight)
        self.noteButton.move(distanceBetweenButtons, self.size().height() - (distanceBetweenButtons + buttonsHeight))
        self.noteButton.resize((self.size().width() - distanceBetweenButtons * 2), buttonsHeight)


    def drawStuff(self, box):
        for i in range(len(self.idTable) - 1):
            for j in range(len(self.idTable[i]) - 1):
                if self.idTable[i][j]:
                    self.layout.removeWidget(i, j)

        if self.currentBox == None and self.windowTitle() == "мусорка" or len(self.upBox) >= 2 and self.upBox[1] == [
            None, "мусорка"]:
            self.isInTrash = True
        else:
            self.isInTrash = False

        if self.windowTitle() == "мусорка":
            boxId = cur.execute("SELECT id FROM stuff WHERE isBox IS 1")
            boxExist = []
            for i in boxId:
                boxExist.append(*i)
            stuff = cur.execute(f"SELECT id, name, isBox FROM stuff WHERE inBox NOT IN ({(', ').join(list(map(str, boxExist)))})")
            self.currentListStuff = []
            for i in stuff:
                self.currentListStuff.append(i)
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
            self.buttons = [[None] * self.widthItem for _ in range(self.highItem)]
            for i in range(self.highItem):
                for j in range(self.widthItem):
                    if self.idTable[i][j] != 0:
                        button = PushButtonRight(self.idTable[i][j][1])
                        button.setFixedSize(80, 80)
                        if self.idTable[i][j][1] == "мусорка" and self.idTable[i][j][0] is None:
                            button.setStyleSheet('background: rgb(191, 191, 191);;')
                            button.left_click.connect(self.leftClickBox)
                            button.right_click.connect(self.rightClickBox)
                        elif self.idTable[i][j][2]:
                            button.setStyleSheet('background: rgb(229, 184, 135);;')
                            button.left_click.connect(self.leftClickBox)
                            button.right_click.connect(self.rightClickBox)
                        else:
                            button.setStyleSheet('background: rgb(245, 222, 179);')
                            button.left_click.connect(self.leftClickItem)
                            button.right_click.connect(self.rightClickItem)
                        self.layout.addWidget(button, i, j)
        else:
            self.buttons = []

    def leftClickBox(self):
        sender = self.sender()
        index = self.layout.indexOf(sender)
        pos = self.layout.getItemPosition(index)
        print(pos)
        self.upBox.append([self.currentBox, self.windowTitle()])
        self.setWindowTitle(self.idTable[pos[0]][pos[1]][1])
        self.currentBox = self.idTable[pos[0]][pos[1]][0]
        self.drawUI()
        self.drawStuff(self.currentBox)
        print(pos[0], pos[1])

    def leftClickItem(self):
        sender = self.sender()
        index = self.layout.indexOf(sender)
        pos = self.layout.getItemPosition(index)
        print(pos)

    def rightClickBox(self):
        print("rightClickBox")

    def rightClickItem(self):
        print("rightClickItem")

    def drawUI(self):
        if self.upBox:
            self.backButton.setVisible(True)
            self.fullBackButton.setVisible(True)
            self.addBoxButton.move(buttonsWidth + distanceBetweenButtons * 2, distanceBetweenButtons)
            self.addItemButton.move(buttonsWidth + distanceBetweenButtons * 2,
                                        buttonsHeight + distanceBetweenButtons * 2)
            self.openRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3, distanceBetweenButtons)
            self.deleteRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3,
                                        buttonsHeight + distanceBetweenButtons * 2)
            self.singleSelectionRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4, distanceBetweenButtons)
            self.multipleSelectionRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4,
                                                   buttonsHeight + distanceBetweenButtons * 2)
            self.executeRadioButton.move(buttonsWidth * 4 + distanceBetweenButtons * 5, distanceBetweenButtons)
            self.planRadioButton.move(buttonsWidth * 4 + distanceBetweenButtons * 5,
                                      buttonsHeight + distanceBetweenButtons * 2)
        else:
            self.backButton.setVisible(False)
            self.fullBackButton.setVisible(False)
            self.addBoxButton.move(distanceBetweenButtons, distanceBetweenButtons)
            self.addItemButton.move(distanceBetweenButtons, buttonsHeight + distanceBetweenButtons * 2)
            self.openRadioButton.move(buttonsWidth * 1 + distanceBetweenButtons * 2, distanceBetweenButtons)
            self.deleteRadioButton.move(buttonsWidth * 1 + distanceBetweenButtons * 2,
                                        buttonsHeight + distanceBetweenButtons * 2)
            self.singleSelectionRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3, distanceBetweenButtons)
            self.multipleSelectionRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3,
                                                   buttonsHeight + distanceBetweenButtons * 2)
            self.executeRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4, distanceBetweenButtons)
            self.planRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4,
                                      buttonsHeight + distanceBetweenButtons * 2)

    def back(self):
        self.setWindowTitle(self.upBox[-1][1])
        self.currentBox = self.upBox[-1][0]
        self.upBox.pop()
        self.drawStuff(self.currentBox)
        self.drawUI()

    def fullBack(self):
        self.setWindowTitle("KilterAndBox")
        self.currentBox = None
        self.upBox.clear()
        self.drawStuff(self.currentBox)
        self.drawUI()

    def addBox(self):
        self.addbox = BOX(self.currentBox)

        self.addbox.show()

    def addItem(self):
        self.additem = ITEM(self.currentBox)
        self.additem.show()

    def reload(self):
        self.drawStuff(self.currentBox)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KilterAndBox()
    # ex.showMaximized()
    ex.show()
    sys.exit(app.exec())