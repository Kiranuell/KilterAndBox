from PyQt5 import Qt, QtWidgets, QtCore


class PushButtonRight(QtWidgets.QPushButton):
    left_click = QtCore.pyqtSignal()
    right_click = QtCore.pyqtSignal()

    def __init__(self, string):
        super().__init__(string)

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.left_click.emit()
            print('left click')
        elif event.button() == Qt.Qt.RightButton:
            self.right_click.emit()
            print('right click')

        QtWidgets.QPushButton.mousePressEvent(self, event)


app = QtWidgets.QApplication([])
window = PushButtonRight('Нажми меня')
window.show()
app.exec_()