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
        
        
class Ellipse:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        rect = QRect(start_point, end_point)
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawEllipse(rect)
        
class Triangle:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()
        x3, y3 = x2, y1
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawPolygon(QPolygonF([QPointF(x1, y1), QPointF(x2, y2), QPointF(x3, y3)]))


class Pentagon:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        center_x, center_y = start_point.x(), start_point.y()
        radius = math.sqrt((end_point.x() - center_x)**2 + (end_point.y() - center_y)**2)
        points = []
        for i in range(5):
            angle_deg = 90 + (360/5)*i
            angle_rad = math.pi * angle_deg / 180
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append(QPointF(x, y))
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawPolygon(QPolygonF(points))
        
class Hexagon:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        center_x, center_y = start_point.x(), start_point.y()
        radius = math.sqrt((end_point.x() - center_x)**2 + (end_point.y() - center_y)**2)
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi * angle_deg / 180
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            points.append(QPointF(x, y))
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawPolygon(QPolygonF(points))
        
                                