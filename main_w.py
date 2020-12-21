import sys
from PyQt5.Qt import *
from PyQt5 import *

from wi_1 import Form1                                             # +++
from wi_2 import Form2                                             # +++

class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()

        self.data = None                                           # +++

        self.leftlist = QListWidget ()
        self.leftlist.insertItem (0, 'form1' )
        self.leftlist.insertItem (1, 'form2' )

        self.stack1 = Form1()

        self.stack1.dialog.signal.connect(self.update_data)        # +++ <<<---

        self.stack2 = Form2()

        self.Stack = QStackedWidget (self)
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.leftlist.currentRowChanged.connect(self.display)
        self.setWindowTitle('StackedWidget demo')
        self.show()

    def display(self,i):
       self.Stack.setCurrentIndex(i)

    def update_data(self, data):                                     # +++ <<<---
         self.data = data
         print(f'Main: {data}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())