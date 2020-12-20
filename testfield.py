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

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 400, 200)
        self.initUI()


    def initUI(self):
        self.button1 = QPushButton(self)
        self.button1.setGeometry(40, 40, 100, 50)
        self.button1.setText("Button 1")



        self.button2 = QPushButton(self)
        self.button2.setGeometry(150, 40, 100, 50)
        self.button2.setText("Button 2")



        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.btn_grp.addButton(self.button1)
        self.btn_grp.addButton(self.button2)



        self.btn_grp.buttonClicked.connect(self.on_click)



        self.show()



    def on_click(self, btn):
        pass # do something with the button clicked



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())