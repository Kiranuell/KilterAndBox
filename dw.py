from PyQt5.Qt import *

class UserDialog(QDialog):
    signal = pyqtSignal(float)

    def __init__(self):
        super(UserDialog, self).__init__()

        vbox = QVBoxLayout(self)
        form = QFormLayout()
        self.data = QDoubleSpinBox()
        form.addRow("Data", self.data)

        buttonbox = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        vbox.addLayout(form)
        vbox.addWidget(buttonbox)

    def accept(self):
        self.signal.emit(self.data.value())
        super().accept()