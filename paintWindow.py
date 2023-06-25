import sys
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow ,QFileDialog
from PyQt5.QtGui import QImage,QPainter,QPen,QCursor,QPixmap,QPainterPath,QBrush
from PyQt5.QtCore import Qt,QPoint
from  ui_paintUI import Ui_MainWindow
import random
from brushes import SolidBrush,Airbrush,CalligraphyBrush,OilBrush,CrayonBrush


class Window(QMainWindow):
    def __init__(self,app) :
        super().__init__()

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Paint with PyQt5")
        self.setGeometry(200, 100, 1000, 800)
        
        self.image=QImage(self.size(),QImage.Format.Format_RGB16)
        self.image.fill(Qt.GlobalColor.white)
        
        self.undo_stack = []
        
        self.drawing=False
        self.brushSize=2
        self.brushColor=Qt.GlobalColor.black
        self.lastPoint=QPoint()
        
        self.eraser_cursor = QCursor(QPixmap("eraser.jpg"))
        self.eraser_mode=False
        self.setCursor(Qt.CrossCursor)
        #brushes   
        self.round_brush = QPainterPath()  
        self.round_brush.addEllipse(-self.brushSize/2, -self.brushSize/2, self.brushSize, self.brushSize)        
        self.square_brush = QPainterPath()  
        self.square_brush.addRect(-self.brushSize/2, -self.brushSize/2, self.brushSize, self.brushSize)
        self.calligraphy_brush = QPainterPath()
        self.calligraphy_brush.lineTo(self.brushSize / 2, self.brushSize / 2)       
        self.spray_can_brush = QPainterPath() 
        self.spray_can_brush.addEllipse(-self.brushSize / 2, -self.brushSize / 2, self.brushSize, self.brushSize)
        self.brush_shape=self.spray_can_brush        
        self.brushOptions = {
            "Solid Brush": SolidBrush,
            "Air Brush": Airbrush,
            "Calligraphy Brush": CalligraphyBrush,
            "Oil Brush": OilBrush,
            "Crayon Brush": CrayonBrush
            }   
        self.selectedBrush="Solid Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]             
        #handling the signals
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionClear.triggered.connect(self.clear)
        self.ui.action3px.triggered.connect(self.three_pixel)
        self.ui.action5px.triggered.connect(self.five_pixel)
        self.ui.action7px.triggered.connect(self.seven_pixel)
        self.ui.action9px.triggered.connect(self.nine_pixel)
        self.ui.action11px.triggered.connect(self.eleven_pixel)
        self.ui.action13px.triggered.connect(self.thirteen_pixel)
        self.ui.actionBlack.triggered.connect(self.black)
        self.ui.actionBlue.triggered.connect(self.blue)
        self.ui.actionRed.triggered.connect(self.red)
        self.ui.actionYellow.triggered.connect(self.yellow)
        self.ui.actionGreen.triggered.connect(self.green)
        self.ui.actionErase.triggered.connect(self.eraser)
        self.ui.actionExit.triggered.connect(sys.exit)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionSolid.triggered.connect(self.solid_brush)
        self.ui.actionAir.triggered.connect(self.air_brush)
        self.ui.actionCalligraphy.triggered.connect(self.calligra_brush)
        self.ui.actionOil.triggered.connect(self.oil_brush)
        self.ui.actionCrayon.triggered.connect(self.crayon_brush)
    
    
    def mousePressEvent(self,event):
        if event.button()==Qt.MouseButton.LeftButton:
            self.drawing=True
            self.lastPoint=event.pos()
            
        self.undo_stack.append(self.image.copy())    

        
        
            
#     def mouseMoveEvent(self,event):
#         if  (event.buttons() & Qt.MouseButton.LeftButton):
#             painter=QPainter(self.image)
#             painter.setPen(QPen(self.brushColor,self.brushSize,Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
#             painter.setBrush(QBrush(self.brushColor,Qt.Dense1Pattern))
#             path = QPainterPath()
#             path.addRect(-self.brushSize/2, -self.brushSize/2, self.brushSize, self.brushSize)
#             path.moveTo(self.lastPoint)
#             path.lineTo(event.pos())
#             painter.drawPath(path)
# # ```         painter.drawLine(self.lastPoint,event.pos()) 
#             self.lastPoint=event.pos()
#         self.update()

 
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            # Create a QPainterPath object to store the brush stroke
            path = QPainterPath()
            path.moveTo(self.lastPoint)

            # Add a series of lines or curves to the path
            for i in range(10):
                # Calculate the direction and distance between the current and previous points
                direction = event.pos() - self.lastPoint
                distance = direction.manhattanLength()

                # Calculate the position of the new point along the path
                t = i / 9
                point = self.lastPoint + direction * t

                # Add a curved line segment to the path
                path.quadTo(self.lastPoint, point)

                # Update the last point to the current point
                self.lastPoint = point
            # self.selectedBrush="Air Brush"
            # # Create a brush object based on the current brush option
            # brushClass = self.brushOptions[self.selectedBrush]
            self.brush = self.brushClass(self.brushColor, self.brushSize)

            # Create a QPainter object and draw the path using the brush
            painter = QPainter(self.image)
            self.brush.draw(painter, path)
            painter.end()

            # Update the display
            self.update()


    def mouseReleaseEvent(self, event):
        if event.button()==Qt.MouseButton.LeftButton:
            self.drawing=False
           
               
    
    def paintEvent(self,event):
        canvasPainter=QPainter(self)
        canvasPainter.drawImage(self.rect(),self.image,self.image.rect())
   
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
        filePath, _ =QFileDialog.getSaveFileName(self,"Save Image","","PNG(*.png);;JPEG(*.jpg,*.jpeg);;All Files(*.*)")
        
        if filePath=="":
            return
        self.image.save(filePath)  
        
    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()    
        
    def three_pixel(self):
        self.brushSize=3    
    def five_pixel(self):
        self.brushSize=5    
    def seven_pixel(self):
        self.brushSize=7    
    def nine_pixel(self):
        self.brushSize=9   
    def eleven_pixel(self):
        self.brushSize=11    
    def thirteen_pixel(self):
        self.brushSize=13 
        
    def black(self):
        self.brushColor=Qt.GlobalColor.black       
    def blue(self):
        self.brushColor=Qt.GlobalColor.blue       
    def red(self):
        self.brushColor=Qt.GlobalColor.red       
    def green(self):
        self.brushColor=Qt.GlobalColor.green      
    def yellow(self):
        self.brushColor=Qt.GlobalColor.yellow   
        
    def eraser(self):
        count=0
        if count % 2 ==0:
           self.brushColor=Qt.GlobalColor.white
           self.brushSize=20
        else:
           self.brushColor=Qt.GlobalColor.black
           self.brushSize=2
        count +=count
     
    def solid_brush(self):
        self.selectedBrush="Solid Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]        
    def air_brush(self):
        self.selectedBrush="Air Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]        
    def calligra_brush(self):
        self.selectedBrush="Calligraphy Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]        
    def oil_brush(self):
        self.selectedBrush="Oil Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]        
    def crayon_brush(self):
        self.selectedBrush="Crayon Brush"
        self.brushClass = self.brushOptions[self.selectedBrush]        
            
     