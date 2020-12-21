import sys
import sqlite3
from PyQt5 import Qt
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QApplication, QRadioButton, QButtonGroup, QSpacerItem
from PyQt5.QtCore import QSize, QRect
from PyQt5 import QtWidgets, QtCore
from Classes import BOX, ITEM, join, split, PushButtonRight, ACCEPTDELETE



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
        self.currentBox = 0
        self.currentListStuff = []
        self.idTable = []
        self.findFlag = False
        oImage = QImage("BoxTexture.jpg")
        sImage = oImage.scaled(QSize(300, 200))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.initUI()
        self.drawStuff(0)

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.setMinimumWidth(500)
        self.setMinimumHeight(295)
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
        self.openRadioButton.setText("делать")

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

        self.cancel = QPushButton(self)
        self.cancel.setVisible(False)
        self.cancel.move(distanceBetweenButtons, buttonsHeight * 2 + distanceBetweenButtons * 3)
        self.cancel.resize(buttonsWidth, buttonsHeight)
        self.cancel.setText("отмена")
        self.cancel.clicked.connect(self.dontFind)
        self.cancel.setStyleSheet('background: rgb(229, 184, 135);')

        self.findButton = QPushButton(self)
        self.findButton.move(distanceBetweenButtons, buttonsHeight * 2 + distanceBetweenButtons * 3)
        self.findButton.resize(buttonsWidth, buttonsHeight)
        self.findButton.setText("найти")
        self.findButton.clicked.connect(self.findStuff)
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

        self.Glayout = Qt.QGridLayout(self)
        self.Glayout.setSpacing(distanceBetweenButtons)

        self.but = QPushButton()
        self.but.resize(50, 50)

        self.Widget = QWidget(self)
        self.Widget.setGeometry(distanceBetweenButtons, distanceBetweenButtons * 4 + buttonsHeight * 3, self.size().width() - distanceBetweenButtons * 2, self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.Widget.setStyleSheet('background: rgb(240, 240, 240);;')

        self.WidgetScroll = QWidget(self)
        self.WidgetScroll.setLayout(self.Glayout)
        self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2 - 10, self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))

        self.Scroll = Qt.QScrollArea(self.Widget)
        self.Scroll.setWidget(self.WidgetScroll)
        self.Scroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2, self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.Scroll.setStyleSheet('background: rgb(240, 240, 240);;')

    def resizeEvent(self, event):
        self.findLineEdit.resize(self.size().width() - (buttonsWidth * 1 + distanceBetweenButtons * 3), buttonsHeight)
        self.noteButton.move(distanceBetweenButtons, self.size().height() - (distanceBetweenButtons + buttonsHeight))
        self.noteButton.resize((self.size().width() - distanceBetweenButtons * 2), buttonsHeight)
        self.Widget.setGeometry(distanceBetweenButtons, distanceBetweenButtons * 4 + buttonsHeight * 3,
                                self.size().width() - distanceBetweenButtons * 2,
                                self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.Scroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))

        hight = 80 * self.highItem + 10 * (self.highItem + 1)
        self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                      hight)
        if hight < self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4):
            self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2 - 19,
                                          self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.moveStuff()

    def drawStuff(self, box):
        while self.Glayout.count():
            child = self.Glayout.takeAt(0)
            if child.widget():
                child.widget().close()

        if self.currentBox == -1 and self.windowTitle() == "архив" or len(self.upBox) >= 2 and self.upBox[1] == [
            -1, "архив"]:
            self.isInTrash = True
        else:
            self.isInTrash = False

        if self.windowTitle() == "архив":
            boxId = cur.execute("SELECT id FROM stuff WHERE isBox IS 1")
            boxExist = [0]
            for i in boxId:
                boxExist.append(*i)
            stuff = cur.execute(f"SELECT id, name, isBox, amount, inBox FROM stuff WHERE inBox NOT IN ({(', ').join(list(map(str, boxExist)))})")
            self.currentListStuff = []
            for i in stuff:
                self.currentListStuff.append(i)
        else:
            stuff = cur.execute("SELECT id, name, isBox, amount, inBox FROM stuff WHERE inBox IS ?", (box,))
            self.currentListStuff = []
            for i in stuff:
                self.currentListStuff.append(i)

        if not self.upBox:
            self.currentListStuff.append([-1, "архив", 1])

        if self.currentListStuff:
            self.widthItem = (self.size().width() - distanceBetweenButtons * 2 + 15) // 95
            if self.widthItem > len(self.currentListStuff):
                self.widthItem = len(self.currentListStuff)
            self.highItem = int((len(self.currentListStuff) / self.widthItem) + 0.99999)
            self.idTable = split(self.currentListStuff, self.widthItem)
            for i in range(self.highItem):
                for j in range(self.widthItem):
                    if self.idTable[i][j] != 0:
                        button = PushButtonRight(self.idTable[i][j][1])
                        button.setFixedSize(80, 80)
                        if self.idTable[i][j][1] == "архив" and self.idTable[i][j][0] == -1:
                            button.setFixedSize(80, 80)
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
                        self.Glayout.addWidget(button, i, j)
            spacerItem = QtWidgets.QSpacerItem(9, 44, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.Glayout.addItem(spacerItem, 0, self.widthItem, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.Glayout.addItem(spacerItem1, self.highItem, 0, 1, 1)
        else:
            self.highItem = 0

    def moveStuff(self):
        while self.Glayout.count():
            child = self.Glayout.takeAt(0)
            if child.widget():
                child.widget().close()

        if self.currentListStuff:
            self.widthItem = (self.size().width() - distanceBetweenButtons * 2 + 15) // 95
            if self.widthItem > len(self.currentListStuff):
                self.widthItem = len(self.currentListStuff)
            self.highItem = int((len(self.currentListStuff) / self.widthItem) + 0.99999)
            self.idTable = split(self.currentListStuff, self.widthItem)
            for i in range(self.highItem):
                for j in range(self.widthItem):
                    if self.idTable[i][j] != 0:
                        button = PushButtonRight(self.idTable[i][j][1])
                        button.setFixedSize(80, 80)
                        if self.idTable[i][j][1] == "архив" and self.idTable[i][j][0] == -1:
                            button.setFixedSize(80, 80)
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
                        self.Glayout.addWidget(button, i, j)
            spacerItem = QtWidgets.QSpacerItem(9, 44, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.Glayout.addItem(spacerItem, 0, self.widthItem, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.Glayout.addItem(spacerItem1, self.highItem, 0, 1, 1)


    def leftClickBox(self):
        sender = self.sender()
        index = self.Glayout.indexOf(sender)
        pos = self.Glayout.getItemPosition(index)
        if self.findFlag:
            print(self.idTable)
            print(self.idTable[pos[0]])
            print(self.idTable[pos[0]][pos[1]])
            self.currentBox = self.idTable[pos[0]][pos[1]][4]
            self.findPath(self.currentBox)
            self.cancel.setVisible(False)
            self.findButton.setVisible(True)
            self.findFlag = False
        else:
            if self.openDeleteButtonGroup.checkedId() == -2:
                self.upBox.append([self.currentBox, self.windowTitle()])
                self.setWindowTitle(self.idTable[pos[0]][pos[1]][1])
                self.currentBox = self.idTable[pos[0]][pos[1]][0]
                self.drawUI()
                self.drawStuff(self.currentBox)
                hight = 80 * self.highItem + 10 * (self.highItem + 1)
                self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                              hight)
                if hight < self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4):
                    self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2 - 19,
                                                  self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))
            else:
                self.delete = ACCEPTDELETE(self.idTable[pos[0]][pos[1]][0], self.idTable[pos[0]][pos[1]][1], self.isInTrash)
                self.delete.show()

    def leftClickItem(self):
        sender = self.sender()
        index = self.Glayout.indexOf(sender)
        pos = self.Glayout.getItemPosition(index)
        if self.findFlag:
            self.currentBox = self.idTable[pos[0]][pos[1]][4]
            self.findPath(self.currentBox)
            self.cancel.setVisible(False)
            self.findButton.setVisible(True)
            self.findFlag = False
        else:
            if self.openDeleteButtonGroup.checkedId() == -2:
                self.addbox = ITEM(self.currentBox, True, self.idTable[pos[0]][pos[1]][0], [self.idTable[pos[0]][pos[1]][1], self.idTable[pos[0]][pos[1]][3]])
                self.addbox.show()
            else:
                self.delete = ACCEPTDELETE(self.idTable[pos[0]][pos[1]][0], self.idTable[pos[0]][pos[1]][1], self.isInTrash)
                self.delete.show()

    def rightClickBox(self):
        sender = self.sender()
        index = self.Glayout.indexOf(sender)
        pos = self.Glayout.getItemPosition(index)
        self.addbox = BOX(self.currentBox, self.idTable[pos[0]][pos[1]][0], self.idTable[pos[0]][pos[1]][1], True)
        self.addbox.show()

    def rightClickItem(self):
        sender = self.sender()
        index = self.Glayout.indexOf(sender)
        pos = self.Glayout.getItemPosition(index)
        self.addbox = ITEM(self.currentBox, False, self.idTable[pos[0]][pos[1]][0], [self.idTable[pos[0]][pos[1]][1], self.idTable[pos[0]][pos[1]][3]], True)
        self.addbox.show()

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
        hight = 80 * self.highItem + 10 * (self.highItem + 1)
        self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                      hight)
        if hight < self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4):
            self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2 - 19,
                                          self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))
        print(self.upBox)

    def fullBack(self):
        self.setWindowTitle("KilterAndBox")
        self.currentBox = 0
        self.upBox.clear()
        self.drawStuff(self.currentBox)
        self.drawUI()
        hight = 80 * self.highItem + 10 * (self.highItem + 1)
        self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                      hight)
        if hight < self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4):
            self.WidgetScroll.setGeometry(0, 0, self.size().width() - distanceBetweenButtons * 2 - 19,
                                          self.size().height() - (distanceBetweenButtons * 6 + buttonsHeight * 4))

    def addBox(self):
        self.addbox = BOX(self.currentBox)
        self.addbox.show()

    def addItem(self):
        self.additem = ITEM(self.currentBox, False)
        self.additem.show()

    def reload(self):
        self.drawStuff(self.currentBox)

    def findStuff(self):
        while self.Glayout.count():
            child = self.Glayout.takeAt(0)
            if child.widget():
                child.widget().close()

        self.findFlag = True
        self.cancel.setVisible(True)
        self.findButton.setVisible(False)

        request = self.findLineEdit.text()
        allStuff = cur.execute("SELECT id, name, isBox, amount, inBox FROM stuff")
        self.currentListStuff = []
        for i in allStuff:
            if request in i[1]:
                self.currentListStuff.append(i)

        if self.currentListStuff:
            print(self.idTable)
            self.widthItem = (self.size().width() - distanceBetweenButtons * 2 + 15) // 95
            if self.widthItem > len(self.currentListStuff):
                self.widthItem = len(self.currentListStuff)
            self.highItem = int((len(self.currentListStuff) / self.widthItem) + 0.99999)
            print(self.idTable)
            self.idTable = split(self.currentListStuff, self.widthItem)
            print(self.idTable)
            for i in range(self.highItem):
                for j in range(self.widthItem):
                    if self.idTable[i][j] != 0:
                        button = PushButtonRight(self.idTable[i][j][1])
                        button.setFixedSize(80, 80)
                        if self.idTable[i][j][1] == "архив" and self.idTable[i][j][0] == -1:
                            button.setFixedSize(80, 80)
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
                        self.Glayout.addWidget(button, i, j)
            spacerItem = QtWidgets.QSpacerItem(9, 44, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.Glayout.addItem(spacerItem, 0, self.widthItem, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.Glayout.addItem(spacerItem1, self.highItem, 0, 1, 1)
        else:
            self.highItem = 0

    def dontFind(self):
        self.cancel.setVisible(False)
        self.findButton.setVisible(True)
        self.drawStuff(self.currentBox)
        self.findFlag = False

    def findPath(self, inBox):
        way = []
        self.currentBox = inBox
        if inBox != 0:
            box = cur.execute("SELECT id, name, inBox FROM stuff Where id = ?", (inBox,))
            data = box.fetchone()
            self.setWindowTitle(data[1])
            needBox = data[2]
            while needBox != 0:
                box = cur.execute("SELECT id, name, inBox FROM stuff Where id = ?", (needBox, ))
                data = box.fetchone()
                way.append([data[0], data[1]])
                needBox = data[2]
            if self.currentBox != 0:
                way.append([0, "KilterAndBox"])
            way.reverse()
            self.upBox = way
            print(self.upBox)
            self.drawStuff(self.currentBox)
            self.drawUI()
        else:
            self.setWindowTitle('KilterAndBox')
            self.upBox = []
            self.drawStuff(self.currentBox)
            self.drawUI()









if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KilterAndBox()
    # ex.showMaximized()
    ex.show()
    sys.exit(app.exec())