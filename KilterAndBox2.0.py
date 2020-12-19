import sys
import sqlite3
from PyQt5 import Qt

from PyQt5 import Qt, QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import *
from Classes import split, join, BOX, ITEM, ACCEPTDELETE, SIGNAL, PushButtonRight
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
        self.fullBackButton.move(distanceBetweenButtons, distanceBetweenButtons)
        self.fullBackButton.resize(buttonsWidth, buttonsHeight)
        self.fullBackButton.setText("на главную")
        self.fullBackButton.setStyleSheet('background: rgb(245, 222, 179);') # предмет
        self.fullBackButton.setStyleSheet('background: rgb(229, 184, 135);') # кнопка или коробка

        self.BackButton = QPushButton(self)
        self.BackButton.move(distanceBetweenButtons, buttonsHeight + distanceBetweenButtons * 2)
        self.BackButton.resize(buttonsWidth, buttonsHeight)
        self.BackButton.setText("назад")
        self.BackButton.setStyleSheet('background: rgb(229, 184, 135);')

        self.addBoxButton = QPushButton(self)
        self.addBoxButton.move(buttonsWidth + distanceBetweenButtons * 2, distanceBetweenButtons)
        self.addBoxButton.resize(buttonsWidth, buttonsHeight)
        self.addBoxButton.setText("нов.коробка")
        self.addBoxButton.setStyleSheet('background: rgb(229, 184, 135);')

        self.BackButton = QPushButton(self)
        self.BackButton.move(buttonsWidth + distanceBetweenButtons * 2, buttonsHeight + distanceBetweenButtons * 2)
        self.BackButton.resize(buttonsWidth, buttonsHeight)
        self.BackButton.setText("нов.предмет")
        self.BackButton.setStyleSheet('background: rgb(229, 184, 135);')

        self.openRadioButton = QRadioButton(self)
        self.openRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3, distanceBetweenButtons)
        self.openRadioButton.resize(buttonsWidth, buttonsHeight)
        self.openRadioButton.setText("открыть")

        self.deleteRadioButton = QRadioButton(self)
        self.deleteRadioButton.move(buttonsWidth * 2 + distanceBetweenButtons * 3,
                                    buttonsHeight + distanceBetweenButtons * 2)
        self.deleteRadioButton.resize(buttonsWidth, buttonsHeight)
        self.deleteRadioButton.setText("удалить")

        self.singleSelectionRadioButton = QRadioButton(self)
        self.singleSelectionRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4, distanceBetweenButtons)
        self.singleSelectionRadioButton.resize(buttonsWidth, buttonsHeight)
        self.singleSelectionRadioButton.setText("единица")

        self.multipleSelectionRadioButton = QRadioButton(self)
        self.multipleSelectionRadioButton.move(buttonsWidth * 3 + distanceBetweenButtons * 4,
                                    buttonsHeight + distanceBetweenButtons * 2)
        self.multipleSelectionRadioButton.resize(buttonsWidth, buttonsHeight)
        self.multipleSelectionRadioButton.setText("множество")

        self.executeRadioButton = QRadioButton(self)
        self.executeRadioButton.move(buttonsWidth * 4 + distanceBetweenButtons * 5, distanceBetweenButtons)
        self.executeRadioButton.resize(buttonsWidth, buttonsHeight)
        self.executeRadioButton.setText("выполнить")

        self.planRadioButton = QRadioButton(self)
        self.planRadioButton.move(buttonsWidth * 4 + distanceBetweenButtons * 5,
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

        self.layout = Qt.QGridLayout()
        # for i in range(10):
        #     for j in range(10):
        #         button = PushButtonRight('{}x{}'.format(i, j))
        #         button.setStyleSheet('background: rgb(229, 184, 135);;')
        #         layout.addWidget(button, i, j)

        widget = Qt.QWidget()
        widget.setLayout(self.layout)

        self.drawStuff(None)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.resize(self.size().width() - distanceBetweenButtons * 2, self.size().height() - (
                                                             distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.centralwidget.move(10, 130)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                                 self.size().height() - (
                                                             distanceBetweenButtons * 6 + buttonsHeight * 4)))
        self.scrollArea.setStyleSheet('background: rgb(240, 240, 240);;')

        self.scrollArea.setWidget(widget)




    def resizeEvent(self, event):
        self.findLineEdit.resize(self.size().width() - (buttonsWidth * 1 + distanceBetweenButtons * 3), buttonsHeight)
        self.noteButton.move(distanceBetweenButtons, self.size().height() - (distanceBetweenButtons + buttonsHeight))
        self.noteButton.resize((self.size().width() - distanceBetweenButtons * 2), buttonsHeight)
        self.centralwidget.resize(self.size().width() - distanceBetweenButtons * 2, self.size().height() - (
                distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                                 self.size().height() - (
                                                         distanceBetweenButtons * 6 + buttonsHeight * 4)))

    def drawStuff(self, box):
        for i in self.buttons:
            for j in i:
                if j:
                    j.deleteLater()

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
                        button = QPushButton(self.idTable[i][j][1])
                        button.setFixedSize(80, 80)
                        if self.idTable[i][j][1] == "мусорка" and self.idTable[i][j][0] is None:
                            button.setStyleSheet('background: rgb(191, 191, 191);;')
                        elif self.idTable[i][j][2]:
                            button.setStyleSheet('background: rgb(229, 184, 135);;')
                        else:
                            button.setStyleSheet('background: rgb(245, 222, 179);')
                        self.layout.addWidget(button, i, j)
        else:
            self.buttons = []



















if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KilterAndBox()
    # ex.showMaximized()
    ex.show()
    sys.exit(app.exec())