
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication
from storage import Storage, Client


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.move(60, 40)

        storage = Storage('server')
        client = storage.select(Client, 'login', 'user3').first()

        self.lbl.setText(f'hello! {client.id}')

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QLineEdit')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
