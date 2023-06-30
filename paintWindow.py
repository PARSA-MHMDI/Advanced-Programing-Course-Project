import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QColorDialog, QVBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QImage, QPainter, QPen, QCursor, QPixmap, QPainterPath, QTransform, QColor
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect, QRectF, QSizeF
from newUI import Ui_MainWindow
from brushes import SolidBrush, Airbrush, CalligraphyBrush, OilBrush, CrayonBrush
from shapes import Rectangle, Circle, StraightLine, Arrow, RoundedRectangle, Ellipse, Triangle, Pentagon, Hexagon
import math
import cv2
import numpy as np


class Window(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Paint")
        self.setGeometry(200, 100, 1400, 850)

        self.image = QImage(self.size(), QImage.Format.Format_RGB16)
        self.image.fill(Qt.GlobalColor.white)
        self.image_path = "./images/save.png"
        # undo redo
        self.undo_stack = []
        self.redo_stack = []
        # zoom
        self.zoom_level = 100
        self.zoom_mode = False

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
        self.ellipse_tool = False
        self.triangle_tool = False
        self.pentagon_tool = False
        self.hexagon_tool = False
        self.shape_flag = False
        self.text_flag = False
        self.text_created = False

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
        self.ui.loadimage_Button.triggered.connect(
            self.change_backgound_picutre)
        self.ui.pen_Button.clicked.connect(self.set_pen)
        self.ui.redo_Button.clicked.connect(self.redo)
        self.ui.all_color_Button.clicked.connect(self.selectColor)
        self.ui.zoom_Button.clicked.connect(lambda: self.zoom(110))

    # Parsa added ========================================
        self.ui.actioncolor_palette.triggered.connect(self.selectColor)
        self.ui.actionredo.triggered.connect(self.redo)
        self.ui.actionBlack_and_White.triggered.connect(
            lambda: self.apply_filter("BW"))
        self.ui.clear_Button.clicked.connect(self.clear)
        self.ui.undo_Button.clicked.connect(self.undo)
        self.ui.save_Button.clicked.connect(self.save)
        self.ui.text_Button.clicked.connect(self.text_mode)
        self.ui.erase_Button.clicked.connect(self.eraser)
        self.ui.line_Button.clicked.connect(self.set_line_tool)
        self.ui.rect_Button.clicked.connect(self.set_rectangle_tool)
        self.ui.circul_Button.clicked.connect(self.set_circle_tool)
        self.ui.arrow_Button.clicked.connect(self.set_arrow_tool)
        self.ui.ellipse_Button.clicked.connect(self.set_ellipse_tool)
        self.ui.triangle_Button.clicked.connect(self.set_triangle_tool)
        self.ui.pentagon_Button.clicked.connect(self.set_pentagon_tool)
        self.ui.hexagon_Button.clicked.connect(self.set_hexagon_tool)

        self.ui.blue_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.blue))
        self.ui.back_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.black))
        self.ui.red_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.red))
        self.ui.green_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.green))
        self.ui.white_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.white))
        self.ui.yellow_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.yellow))
        self.ui.purple_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.darkMagenta))
        self.ui.pink_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.magenta))
        self.ui.darkYellow_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.darkYellow))
        self.ui.lightGray_Button.clicked.connect(
            lambda: self.change_brush_color(Qt.GlobalColor.lightGray))

        self.ui.pen_Button_2.clicked.connect(self.solid_brush)
        self.ui.air_Button.clicked.connect(self.air_brush)
        self.ui.oil_Button.clicked.connect(self.oil_brush)
        self.ui.clalligraphy_Button.clicked.connect(self.calligra_brush)
        self.ui.crayon_Button.clicked.connect(self.crayon_brush)
        self.ui.size_Slider.valueChanged.connect(self.value_changed)
        self.ui.flip_Button.clicked.connect(self.flip)
        self.ui.loadimage_Button.clicked.connect(self.change_backgound_picutre)
        self.ui.flip_up.clicked.connect(self.flip_up)
        self.ui.rotate_Button.clicked.connect(self.rotate)
        self.ui.loadimage_Button_2.clicked.connect(
            lambda: self.apply_filter("orginal"))
        self.ui.blackwhite_Button.clicked.connect(
            lambda: self.apply_filter("BW"))
        self.ui.invert_Button.clicked.connect(
            lambda: self.apply_filter("invert"))
        self.ui.sepia_Button.clicked.connect(
            lambda: self.apply_filter("sepia"))
        self.ui.HDR_Button.clicked.connect(
            lambda: self.apply_filter("HDR"))
        self.ui.resize_button.clicked.connect(self.resize_button)

        # =================== Change UI ================================
        # Adding some labels to bottom toolbar
        self.ui.toolBar.addSeparator()

        self.ui.size_label_toolbar = QtWidgets.QLabel("Size is: 1 px")
        self.ui.size_label_toolbar.adjustSize()
        self.ui.size_label_toolbar.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.toolBar.addWidget(self.ui.size_label_toolbar)

        self.ui.toolBar.addSeparator()

        self.ui.length_label = QtWidgets.QLabel()
        self.ui.length_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.toolBar.addWidget(self.ui.length_label)

        self.ui.toolBar_2.setStyleSheet(
            "background-color: rgb(230, 230, 230);")

        self.ui.toolBar.setStyleSheet(
            "background-color: rgb(230, 230, 230);")

        self.ui.toolBar.addSeparator()

        self.pos_label = QtWidgets.QLabel()
        self.pos_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pos_label.setObjectName("pos_label")
        self.pos_label.setText(" Mouse position is: ")
        self.ui.toolBar.addWidget(self.pos_label)

        # In here we want to set Icon for appication
        app_icon = QtGui.QIcon()
        app_icon.addPixmap(QtGui.QPixmap("./images/paint.png"),
                           QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(app_icon)

        # Changing background of spinBox to white
        self.ui.width_spinBox.setStyleSheet(
            "background-color: rgb(255, 255, 255);")
        self.ui.height_spinBox.setStyleSheet(
            "background-color: rgb(255, 255, 255);")

        # change fram and tabbar size
        self.ui.frame.setGeometry(
            0, 0, self.size().width(), 112)

        # chage button back_ground
        self.ui.resize_button.setStyleSheet(
            "background-color: rgb(220, 220, 220);")

        self.ui.width_spinBox.setRange(0, 10000)
        self.ui.height_spinBox.setRange(0, 10000)

        # ===================================================

    def value_changed(self, value):
        self.brushSize = value
        self.ui.size_label_toolbar.setText(f"Size is: {value} px")
        self.ui.size_label_toolbar.adjustSize()

    def change_backgound_picutre(self):
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        loaded_image = QtGui.QImage(self.image_path)
        # self.image = loaded_image
        self.image = loaded_image.scaled(
            self.size().width() - 100, self.size().height())
        self.update()
        # For Exit warrning

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Exit Confirmation", "Do you want to save?",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.save()
            if type(event) == bool:  # For pushing exit button
                sys.exit()
        elif reply == QMessageBox.No:
            sys.exit()

        elif reply == QMessageBox.Cancel:
            event.ignore()

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

        elif kind == "Ellipse":
            Radius = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                     pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"Radius is: {Radius}")

        elif kind == "Triangle":
            Diameter = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                       pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"Diameter is: {Diameter}")

        elif kind == "Pentagon":
            Diameter = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                       pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"Diameter is: {Diameter}")

        elif kind == "Hexagon":
            Diameter = round(math.sqrt(pow((start.x() - end.x()), 2) +
                                       pow((start.y() - end.y()), 2)), 1)
            self.ui.length_label.setText(f"Diameter is: {Diameter}")

    def apply_filter(self, mood):
        """This function applies filters to images

        Args:
            mood (str): which filter
            path (srt): where is the image
        """
        if mood == "BW":
            self.image = self.image.convertToFormat(
                QtGui.QImage.Format_Grayscale8)

        elif mood == "orginal":
            loaded_image = QtGui.QImage(self.image_path)
            self.image = loaded_image.scaled(self.size())
        elif mood == "invert":
            inverted_image = self.image.copy()
            for y in range(inverted_image.height()):
                for x in range(inverted_image.width()):
                    pixel_color = QColor(inverted_image.pixel(x, y))
                    inverted_color = QColor(
                        255 - pixel_color.red(), 255 - pixel_color.green(), 255 - pixel_color.blue())
                    inverted_image.setPixel(x, y, inverted_color.rgb())
            self.image = inverted_image
        elif mood == "sepia":
            sepia_image = self.image.copy()
            for y in range(sepia_image.height()):
                for x in range(sepia_image.width()):
                    pixel_color = QColor(sepia_image.pixel(x, y))
                    red = int(0.393 * pixel_color.red() + 0.769 *
                              pixel_color.green() + 0.189 * pixel_color.blue())
                    green = int(0.349 * pixel_color.red() + 0.686 *
                                pixel_color.green() + 0.168 * pixel_color.blue())
                    blue = int(0.272 * pixel_color.red() + 0.534 *
                               pixel_color.green() + 0.131 * pixel_color.blue())
                    sepia_color = QColor(min(red, 255), min(
                        green, 255), min(blue, 255))
                    sepia_image.setPixel(x, y, sepia_color.rgb())
            self.image = sepia_image

        elif mood == "HDR":
            hdr_image = self.image.copy()
            for y in range(hdr_image.height()):
                for x in range(hdr_image.width()):
                    pixel_color = QColor(hdr_image.pixel(x, y))
                    red = min(2 * pixel_color.red(), 255)
                    green = min(2 * pixel_color.green(), 255)
                    blue = min(2 * pixel_color.blue(), 255)
                    hdr_color = QColor(red, green, blue)
                    hdr_image.setPixel(x, y, hdr_color.rgb())
            self.image = hdr_image
        self.update()

    # End Parsa added======================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True

            self.startPoint = event.pos()

            self.lastPoint = event.pos()

        self.undo_stack.append(self.image.copy())

        # This line is for updating mouse position
        self.pos_label.setText(
            f" Mouse position is: X:{event.pos().x()}, Y:{event.pos().y()}")

        if self.text_flag:
            self.text_created = True
            text, ok = QtWidgets.QInputDialog.getText(
                self, 'Enter Text', 'Enter your text:')
            if ok:
                # Create a text box at the clicked position
                self.text_box = QLineEdit(self)
                self.text_box.setText(text)
                self.text_box.move(event.pos())
                self.text_box.returnPressed.connect(
                    lambda: self.draw_text(self.text_box))
                self.text_box.show()
            self.text_flag = False

    def draw_text(self, text_box):
        self.text_created = True
        # Draw the text on the canvas
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brushColor, self.brushSize,
                       Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawText(text_box.pos(), text_box.text())
        painter.end()
        self.update()

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

        # This line is for updating mouse position
        self.pos_label.setText(
            f" Mouse position is: X:{event.pos().x()}, Y:{event.pos().y()}")

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
            elif self.ellipse_tool:
                self.draw_ellipse(self.startPoint, self.endPoint)
            elif self.triangle_tool:
                self.draw_triangle(self.startPoint, self.endPoint)
            elif self.hexagon_tool:
                self.draw_hexagon(self.startPoint, self.endPoint)
            elif self.pentagon_tool:
                self.draw_pentagon(self.startPoint, self.endPoint)
        # for add text
        if self.text_flag:
            rect = QRect(self.endPoint, QPoint())  # Convert QPoint to QRect
            self.text_edit.setGeometry(rect)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.get_zoomed_image(),
                          self.get_zoomed_image().rect())

    def set_eraser_mode(self, enabled):
        self.eraser_mode = enabled

        if enabled:
            self.setCursor(self.eraser_cursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def undo(self):
        if len(self.undo_stack) > 0:
            prev_image = self.undo_stack.pop()
            self.redo_stack.append(self.image.copy())

            self.image = prev_image.copy()

            self.update()

    def redo(self):
        if len(self.redo_stack) > 0:
            next_image = self.redo_stack.pop()
            self.undo_stack.append(self.image.copy())
            self.image = next_image.copy()
            self.update()

    # Parsa Added

    def text_mode(self):
        # Set the text_flag to True when the "Text" button is clicked
        self.text_flag = True

    def text(self):
        self.set_default()
        self.text_edit = QTextEdit(self)
        self.text_flag = True

    def flip(self):
        self.image = self.image.mirrored(vertical=False, horizontal=True)
        self.update()

    def flip_up(self):
        self.image = self.image.mirrored(vertical=True, horizontal=False)
        self.update()

    def rotate(self):
        angle = 90  # Define the rotation angle
        transform = QTransform().rotate(angle)
        self.image = self.image.transformed(transform)
        self.update()

    def resize_button(self):
        width = self.ui.width_spinBox.value()
        heigth = self.ui.height_spinBox.value()

        self.image = self.image.scaled(width, heigth)
        self.update()

    # End Parsa Added

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg,*.jpeg);;All Files(*.*)")

        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        # Clear the text
        if self.text_created:
            self.text_box.clear()
            # self.text_box.setPlainText("")  # Clear the text edit
            self.text_box.hide()  # Hide the text edit widget

            self.text_flag = False  # Reset the text flag
            self.text_created = False
            self.undo_stack = []
        self.update()

    def change_brush_size(self, size):
        self.value_changed(size)
        self.ui.size_Slider.setValue(size)  # For changing slider value

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
        self.zoom_mode = False
        self.rectangle_tool = False
        self.circle_tool = False
        self.line_tool = False
        self.arrow_tool = False
        self.shape_flag = False
        self.roundedcircle_tool = False
        self.ellipse_tool = False
        self.triangle_tool = False
        self.pentagon_tool = False
        self.hexagon_tool = False

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

    def set_ellipse_tool(self):
        self.set_default()
        self.ellipse_tool = True
        self.shape_flag = True

    def set_triangle_tool(self):
        self.set_default()
        self.triangle_tool = True
        self.shape_flag = True

    def set_pentagon_tool(self):
        self.set_default()
        self.pentagon_tool = True
        self.shape_flag = True

    def set_hexagon_tool(self):
        self.set_default()
        self.hexagon_tool = True
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

    def draw_ellipse(self, start_point, end_point):
        ellipse = Ellipse(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        ellipse.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "Ellipse")

    def draw_triangle(self, start_point, end_point):
        triangle = Triangle(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        triangle.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "Triangle")

    def draw_pentagon(self, start_point, end_point):
        pentagon = Pentagon(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        pentagon.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "Pentagon")

    def draw_hexagon(self, start_point, end_point):
        hexagon = Hexagon(self.brushColor, self.brushSize)
        painter = QPainter(self.image)
        hexagon.draw(painter, start_point, end_point)
        painter.end()
        self.update()
        self.find_length(start_point, end_point, "Hexagon")

    def set_pen(self):
        self.zoom(100)
        self.set_default()
        self.brushColor = Qt.GlobalColor.black
        self.brushSize = 2
        self.brushClass = self.brushOptions["Solid Brush"]

    def selectColor(self):
        color = QColorDialog.getColor(
            self.brushColor, self, options=QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.brushColor = color

    def zoom(self, zoom_level):
        self.zoom_level = zoom_level
        self.update()

    def get_zoomed_image(self):
        # Calculate the zoomed image based on the current zoom level
        zoom_factor = self.zoom_level / 100.0
        zoomed_size = QSizeF(self.image.width() * zoom_factor,
                             self.image.height() * zoom_factor)

        # Calculate the position of the zoomed image to center it within the widget
        x = (self.width() - zoomed_size.width()) / 2
        y = (self.height() - zoomed_size.height()) / 2

        # Create a QRectF object to represent the visible area of the widget
        visible_rect = QRectF(0, 0, self.width(), self.height())

        # Create a QRectF object to represent the zoomed image
        zoomed_rect = QRectF(x, y, zoomed_size.width(), zoomed_size.height())

        # Create a QImage object for the zoomed image
        zoomed_image = QImage(self.size(), QImage.Format_ARGB32)
        zoomed_image.fill(Qt.transparent)

        # Draw the zoomed image to the QImage object
        painter = QPainter(zoomed_image)
        painter.drawImage(zoomed_rect, self.image, visible_rect)
        painter.end()

        return zoomed_image

    def wheelEvent(self, event):
        # Handle mouse wheel events to zoom in and out
        if event.angleDelta().y() > 0:
            # Increase zoom level by 10%
            self.zoom(min(self.zoom_level + 10, 400))
        else:
            # Decrease zoom level by 10%
            self.zoom(max(self.zoom_level - 10, 10))
