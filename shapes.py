from PyQt5.QtGui import QPen,QPolygonF
from PyQt5.QtCore import QRect,QPointF,QRectF
import math

class Rectangle:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        rect = QRect(start_point, end_point)
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawRect(rect)

class Circle:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, center_point, radius):
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawEllipse(center_point, radius, radius)
        
class StraightLine:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawLine(start_point, end_point)
        
class Arrow:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawLine(start_point, end_point)
        polygon = QPolygonF()
        polygon.append(QPointF(end_point))
        angle = math.atan2(end_point.y() - start_point.y(), end_point.x() - start_point.x())
        polygon.append(QPointF(end_point.x() - 20 * math.cos(angle + math.pi / 6), end_point.y() - 20 * math.sin(angle + math.pi / 6)))
        polygon.append(QPointF(end_point.x() - 20 * math.cos(angle - math.pi / 6), end_point.y() - 20 * math.sin(angle - math.pi / 6)))
        painter.drawPolygon(polygon)
        
class RoundedRectangle:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        rect = QRectF(start_point, end_point)
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawRoundedRect(rect, 20, 20)                        