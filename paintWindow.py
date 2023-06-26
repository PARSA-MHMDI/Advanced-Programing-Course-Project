import sys
import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPainter, QPen, QCursor, QPixmap, QPainterPath, QBrush, QCloseEvent
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect, QSize
from ui_paintUI import Ui_MainWindow
import random
from brushes import SolidBrush, Airbrush, CalligraphyBrush, OilBrush, CrayonBrush
from shapes import Rectangle, Circle, StraightLine, Arrow, RoundedRectangle
import math
import cv2
import numpy as np


class Rectangle:
    def __init__(self, color, thickness):
        self.color = color
        self.thickness = thickness

    def draw(self, painter, start_point, end_point):
        rect = QRect(start_point, end_point)
        painter.setPen(QPen(self.color, self.thickness))
        painter.drawRect(rect)


class Window(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Paint with PyQt5")
        self.setGeometry(200, 100, 1000, 800)

        self.image = QImage(self.size(), QImage.Format.Format_RGB16)
        self.image.fill(Qt.GlobalColor.white)
        self.image_path = "./images/save.png"

        self.undo_stack = []

        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.GlobalColor.black
        self.lastPoint = QPoint()

        self.eraser_cursor = QCursor(QPixmap("eraser.jpg"))
        self.eraser_mode = False
        self.setCursor(Qt.CrossCursor)

        # shapes
        self.rectangle_tool = False
        self.circle_tool = False
        self.line_tool = False
        self.arrow_tool = False
        self.roundedcircle_tool = False
        self.shape_flag = False

        # brushes
        self.round_brush = QPainterPath()
        self.round_brush.addEllipse(-self.brushSize/2, -
                                    self.brushSize/2, self.brushSize, self.brushSize)
        self.square_brush = QPainterPath()
        self.square_brush.addRect(-self.brushSize/2, -
                                  self.brushSize/2, self.brushSize, self.brushSize)
        self.calligraphy_brush = QPainterPath()
        self.calligraphy_brush.lineTo(self.brushSize / 2, self.brushSize / 2)
        self.spray_can_brush = QPainterPath()
        self.spray_can_brush.addEllipse(-self.brushSize / 2, -
                                        self.brushSize / 2, self.brushSize, self.brushSize)
        self.brush_shape = self.spray_can_brush
        self.brushOptions = {
            "Solid Brush": SolidBrush,
            "Air Brush": Airbrush,
            "Calligraphy Brush": CalligraphyBrush,
            "Oil Brush": OilBrush,
            "Crayon Brush": CrayonBrush
        }
        self.selectedBrush = "Solid Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]
        # handling the signals
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionClear.triggered.connect(self.clear)
        self.ui.action3px.triggered.connect(lambda: self.change_brush_size(3))
        self.ui.action5px.triggered.connect(lambda: self.change_brush_size(5))
        self.ui.action7px.triggered.connect(lambda: self.change_brush_size(7))
        self.ui.action9px.triggered.connect(lambda: self.change_brush_size(9))
        self.ui.action11px.triggered.connect(
            lambda: self.change_brush_size(11))
        self.ui.action13px.triggered.connect(
            lambda: self.change_brush_size(13))
        self.ui.actionBlack.triggered.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.black))
        self.ui.actionBlue.triggered.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.blue))
        self.ui.actionRed.triggered.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.red))
        self.ui.actionYellow.triggered.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.yellow))
        self.ui.actionGreen.triggered.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.green))
        self.ui.actionErase.triggered.connect(self.eraser)
        self.ui.actionExit.triggered.connect(self.closeEvent)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionSolid.triggered.connect(self.solid_brush)
        self.ui.actionAir.triggered.connect(self.air_brush)
        self.ui.actionCalligraphy.triggered.connect(self.calligra_brush)
        self.ui.actionOil.triggered.connect(self.oil_brush)
        self.ui.actionCrayon.triggered.connect(self.crayon_brush)
        self.ui.actionRectangle.triggered.connect(self.set_rectangle_tool)
        self.ui.actionCircle.triggered.connect(self.set_circle_tool)
        self.ui.actionline.triggered.connect(self.set_line_tool)
        self.ui.actionArrow.triggered.connect(self.set_arrow_tool)
        self.ui.actionRoundedRectangle.triggered.connect(
            self.set_roundedcircle_tool)
        self.ui.actionChangeImage.triggered.connect(
            self.change_backgound_picutre)

    # Parsa added ========================================
        # For silder
        self.ui.slider.valueChanged.connect(self.value_changed)
        self.ui.actionBlackandWhite.triggered.connect(
            lambda: self.apply_filter("BW"))

    def value_changed(self, value):
        self.brushSize = value
        self.ui.size_label.setText(f"Size is: {value} px")
        self.ui.size_label.adjustSize()

    def change_backgound_picutre(self):
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        loaded_image = QtGui.QImage(self.image_path)
        self.image = loaded_image.scaled(self.size())
        self.update()
        # For Exit warrning

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit Confirmation", "Do you want to save?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save()
            if type(event) == bool:  # For pushing exit button
                sys.exit()
        else:
            sys.exit()

    def find_length(self, start, end, kind: str):
        """This function will find length of each shape

        Args:
            start (PyQt5.QtCore.QPoint): start point
            end (PyQt5.QtCore.QPoint): End point or Radius
            kind (str): name of shape
        """

        if kind == "StraightLine":
            length = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                     pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"length is: {length}")

        elif kind == "Rectangle":
            Diameter = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                       pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"Diameter is: {Diameter}")

        elif kind == "Circle":
            Radius = end
            self.ui.length_label.setText(f"Radius is: {Radius}")

        elif kind == "Arrow":
            length = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                     pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"length is: {length}")

        elif kind == "RoundedRectangle":
            Diameter = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                       pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"Diameter is: {Diameter}")

    def apply_filter(self, mood):
        if mood == "BW":
            self.image = self.image.convertToFormat(
                QtGui.QImage.Format_Grayscale8)
        self.update()

    # End Parsa added======================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

            self.startPoint = event.pos()

        self.undo_stack.append(self.image.copy())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if not self.shape_flag:
                path = QPainterPath()
                path.moveTo(self.lastPoint)

                for i in range(10):
                    direction = event.pos() - self.lastPoint
                    distance = direction.manhattanLength()
                    t = i / 9
                    point = self.lastPoint + direction * t
                    path.quadTo(self.lastPoint, point)
                    self.lastPoint = point

                self.brush = self.brushClass(self.brushColor, self.brushSize)

                painter = QPainter(self.image)
                self.brush.draw(painter, path)
                painter.end()

        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

            self.endPoint = event.pos()
            self.radius = int(math.sqrt((self.endPoint.x() - self.startPoint.x())
                              ** 2 + (self.endPoint.y() - self.startPoint.y()) ** 2) / 2)

            # calculate center point as midpoint of start and end points
            self.center_point = QPointF((self.startPoint.x(
            ) + self.endPoint.x()) / 2, (self.startPoint.y() + self.endPoint.y()) / 2)

            # convert center point to QPoint
            self.center_point = QPoint(
                int(self.center_point.x()), int(self.center_point.y()))

        if self.shape_flag:
            if self.rectangle_tool:
                self.draw_rectangle(self.startPoint, self.endPoint)
            elif self.circle_tool:
                self.draw_circle(self.center_point, self.radius)
            elif self.line_tool:
                self.draw_line(self.startPoint, self.endPoint)
            elif self.arrow_tool:
                self.draw_arrow(self.startPoint, self.endPoint)
            elif self.roundedcircle_tool:
                self.draw_rounded_rectangle(self.startPoint, self.endPoint)

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def set_eraser_mode(self, enabled):
        self.eraser_mode = enabled

        if enabled:
            self.setCursor(self.eraser_cursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def undo(self):
        if len(self.undo_stack) > 0:
            # pop the previous image from the undo stack
            prev_image = self.undo_stack.pop()

            # set the current image to the previous image
            self.image = prev_image.copy()

            # redraw the image
            self.update()

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg,*.jpeg);;All Files(*.*)")

        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.undo_stack = []
        self.update()

    def change_brush_size(self, size):
        self.value_changed(size)
        self.ui.slider.setValue(size)  # For changing slider value

    def change_brush_color(self, color):
        self.brushColor = color

    def eraser(self):
        self.set_default()
        self.brushColor = Qt.GlobalColor.white
        self.brushSize = 15
        self.brushClass = self.brushOptions["Solid Brush"]

    def solid_brush(self):
        self.set_default()
        self.selectedBrush = "Solid Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]

    def air_brush(self):
        self.set_default()
        self.set_default()
        self.selectedBrush = "Air Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]

    def calligra_brush(self):
        self.set_default()
        self.set_default()
        self.selectedBrush = "Calligraphy Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]

    def oil_brush(self):
        self.set_default()
        self.selectedBrush = "Oil Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]

    def crayon_brush(self):
        self.set_default()
        self.selectedBrush = "Crayon Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]

    def set_default(self):
        self.rectangle_tool = False
        self.rectangle_tool = False
        self.circle_tool = False
        self.line_tool = False
        self.arrow_tool = False
        self.shape_flag = False

    def set_rectangle_tool(self):
        self.set_default()
        self.rectangle_tool = True
        self.shape_flag = True

    def set_rectangle_tool(self):
        self.set_default()
        self.rectangle_tool = True
        self.shape_flag = True

    def set_circle_tool(self):
        self.set_default()
        self.circle_tool = True
        self.shape_flag = True

    def set_line_tool(self):
        self.set_default()
        self.line_tool = True
        self.shape_flag = True

    def set_arrow_tool(self):
        self.set_default()
        self.arrow_tool = True
        self.shape_flag = True

    def set_roundedcircle_tool(self):
        self.set_default()
        self.roundedcircle_tool = True
        self.shape_flag = True

    def draw_rectangle(self, start_point, end_point):
        rect = Rectangle(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        rect.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "Rectangle")

    def draw_circle(self, center_point, radius):
        circle = Circle(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        circle.draw(painter, center_point, radius)
        painter.end()
        self.update()
        self.find_length(center_point, radius, "Circle")

    def draw_line(self, start_point, end_point):
        line = StraightLine(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        line.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "StraightLine")

    def draw_arrow(self, start_point, end_point):
        arrow = Arrow(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        arrow.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "Arrow")

    def draw_rounded_rectangle(self, start_point, end_point):
        rect = RoundedRectangle(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        rect.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "RoundedRectangle")
