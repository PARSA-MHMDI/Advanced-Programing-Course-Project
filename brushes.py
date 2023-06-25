from PyQt5.QtGui import QPen,QBrush
from PyQt5.QtCore import Qt,QPoint
import random

class Brush:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def draw(self, painter, path):
        raise NotImplementedError


class SolidBrush(Brush):
    def draw(self, painter, path):
        painter.setPen(QPen(self.color, self.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(self.color))
        painter.drawPath(path)


class Airbrush(Brush):
    def draw(self, painter, path):
        for i in range(100):
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            painter.setPen(QPen(self.color, 1))
            painter.drawPoint(path.currentPosition() + QPoint(x, y))


class CalligraphyBrush(Brush):
    def draw(self, painter, path):
        for i in range(100):
            t = i / 99
            width = self.size * (1 - t) + 1 * t
            painter.setPen(QPen(self.color, width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPoint(path.pointAtPercent(t))


class OilBrush(Brush):
    def draw(self, painter, path):
        for i in range(10):
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            painter.setPen(QPen(self.color, self.size))
            painter.drawPoint(path.currentPosition() + QPoint(x, y))


class CrayonBrush(Brush):
    def draw(self, painter, path):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        for i in range(10):
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            path.addEllipse(path.currentPosition() + QPoint(x, y), self.size / 2, self.size / 2)
        painter.drawPath(path)