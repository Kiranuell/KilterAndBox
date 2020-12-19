from PyQt5 import Qt


app = Qt.QApplication([])

layout = Qt.QGridLayout()

for i in range(10):
    for j in range(5):
        button = Qt.QPushButton('{}x{}'.format(i, j))
        layout.addWidget(button, i, j)

w = Qt.QWidget()
w.setLayout(layout)

mw = Qt.QScrollArea()
mw.setWidget(w)
mw.resize(500, 500)
mw.show()

app.exec()