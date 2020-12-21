from PyQt5.Qt import *

class Form2(QWidget):
    def __init__(self):
        super(Form2, self).__init__()

        self.setWindowTitle('Form2')
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("form2"))
        self.setLayout(hbox2)

        self.data = 0
        self.data = 0