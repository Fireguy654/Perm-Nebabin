import sys

from addEditCoffeeForm import Ui_Dialog
from mainui import Ui_Form

from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
import sqlite3


class TableChange(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setModal(True)

        self.initUI()

    def initUI(self):
        self.con = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.con.cursor()

        self.add.clicked.connect(self.insert_in_db)
        self.change.clicked.connect(self.upd_db)

    def get_info(self):
        names = []
        values = []
        if self.name.text() != '':
            names.append('name')
            values.append('"' + self.name.text() + '"')
        if self.roasting.text() != '':
            names.append('roasting')
            values.append('"' + self.roasting.text() + '"')
        if self.form.text() != '':
            names.append('form')
            values.append('"' + self.form.text() + '"')
        if self.description.text() != '':
            names.append('description')
            values.append('"' + self.description.text() + '"')
        if self.cost.value() != 0:
            names.append('cost')
            values.append(str(self.cost.value()))
        if self.volume.value() != 0:
            names.append('volume')
            values.append(str(self.volume.value()))
        return names, values

    def insert_in_db(self):
        names, values = self.get_info()
        if not len(names):
            return
        query = f'INSERT INTO coffee ({", ".join(names)})  VALUES ({", ".join(values)})'
        self.con.cursor().execute(query)
        self.con.commit()

    def upd_db(self):
        names, values = self.get_info()
        if not len(names):
            return
        tmp = []
        query = f'UPDATE coffee\nSET '
        for i in range(len(names)):
            tmp.append(names[i] + '=' + values[i])
        query += f'{", ".join(tmp)}\nWHERE id={self.id.value()}'
        self.con.cursor().execute(query)
        self.con.commit()


class Table(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data/coffee.sqlite')
        self.db.open()

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('coffee')
        self.model.select()

        self.view.setModel(self.model)
        self.view.clicked.connect(self.upd)

        self.setWindowTitle('Таблица кофе')

        self.btn.clicked.connect(self.change)

    def upd(self):
        self.model.select()

    def change(self):
        self.tmp = TableChange()
        self.tmp.exec()
        self.upd()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Table()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
