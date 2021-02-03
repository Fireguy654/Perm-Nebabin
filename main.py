import sys

from PyQt5 import uic
from PyQt5.QtSql import *
from PyQt5.QtWidgets import *


class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('coffee.sqlite')
        self.db.open()

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('coffee')
        self.model.select()

        self.view.setModel(self.model)

        self.setWindowTitle('Таблица кофе')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Table()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
