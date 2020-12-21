from PyQt5.Qt import *
from dw import UserDialog


class Form1(QWidget):
    def __init__(self):
        super(Form1, self).__init__()

        self.data = None                                               # +++

        self.setWindowTitle('Form1')
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("form1"))

        add_btn = QPushButton("Add data")
        add_btn.clicked.connect(self.add)
        hbox1.addWidget(add_btn)
        self.setLayout(hbox1)

        self.dialog = UserDialog()                                     # +++
        self.dialog.signal.connect(self.signal_handler)                # +++

    def add(self):
#       self.dialog = UserDialog()
#       self.dialog.signal.connect(self.signal_handler)
       self.dialog.show()

    def signal_handler(self, data):
         self.data = data
         print(data)