import sys
import sqlite3
from PyQt5 import Qt, QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import *
from Classes import split, join, BOX, ITEM, ACCEPTDELETE, SIGNAL
from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5 import QtWidgets, uic


distanceBetweenButtons = 10
buttonsHeight = 30
buttonsWidth = 80

con = sqlite3.connect("testbox.db")
cur = con.cursor()

class KilterAndBox(QWidget):
    def __init__(self):
        super().__init__()
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

        self.singleMultipleButtonGroup = QButtonGroup()
        self.singleMultipleButtonGroup.addButton(self.singleSelectionRadioButton)
        self.singleMultipleButtonGroup.addButton(self.multipleSelectionRadioButton)

        self.executePlanDeleteButtonGroup = QButtonGroup()
        self.executePlanDeleteButtonGroup.addButton(self.executeRadioButton)
        self.executePlanDeleteButtonGroup.addButton(self.planRadioButton)

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

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.resize(self.size().width() - distanceBetweenButtons * 2, self.size().height() - (
                                                             distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.centralwidget.move(10, 130)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                                 self.size().height() - (
                                                             distanceBetweenButtons * 6 + buttonsHeight * 4)))
        self.scrollArea.setStyleSheet('background: rgb(240, 240, 240);;')


        self.Button = QtWidgets.QPushButton()
        self.Button.resize(80, 80)
        self.Button.setGeometry(QtCore.QRect(10, 10, 80, 80))
        self.scrollArea.setWidget(self.Button)



        # self.scrollAreaWidgetContents = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 100000, 100000))
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)



    def resizeEvent(self, event):
        self.findLineEdit.resize(self.size().width() - (buttonsWidth * 1 + distanceBetweenButtons * 3), buttonsHeight)
        self.noteButton.move(distanceBetweenButtons, self.size().height() - (distanceBetweenButtons + buttonsHeight))
        self.noteButton.resize((self.size().width() - distanceBetweenButtons * 2), buttonsHeight)
        self.centralwidget.resize(self.size().width() - distanceBetweenButtons * 2, self.size().height() - (
                distanceBetweenButtons * 6 + buttonsHeight * 4))
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, self.size().width() - distanceBetweenButtons * 2,
                                                 self.size().height() - (
                                                         distanceBetweenButtons * 6 + buttonsHeight * 4)))



















if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KilterAndBox()
    # ex.showMaximized()
    ex.show()
    sys.exit(app.exec())