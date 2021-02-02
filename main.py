import random
import sys

from PyQt5 import uic, QtGui
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.circles = []

        self.initUI()

    def initUI(self):
        uic.loadUi('UI.ui', self)

        self.btn.clicked.connect(self.add_circle)

    def add_circle(self):
        self.circles.append((random.randint(1, 900), random.randint(1, 700), random.randint(1, 50)))
        self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        self.paint_circles(qp)
        qp.end()

    def paint_circles(self, qp):
        for i in self.circles:
            qp.setPen(QColor(255, 255, 0))
            qp.drawEllipse(i[0] - i[2], i[1] - i[2], i[2] * 2, i[2] *2)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
