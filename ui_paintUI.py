# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paintUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1098, 799)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1098, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuBrushSize = QtWidgets.QMenu(self.menubar)
        self.menuBrushSize.setObjectName("menuBrushSize")
        self.menuBrushColor = QtWidgets.QMenu(self.menubar)
        self.menuBrushColor.setObjectName("menuBrushColor")
        self.menuBrushes = QtWidgets.QMenu(self.menubar)
        self.menuBrushes.setObjectName("menuBrushes")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setVisible(True)
        self.actionSave.setObjectName("actionSave")
        self.actionClear = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/clear.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear.setIcon(icon1)
        self.actionClear.setObjectName("actionClear")
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/exit 2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon2)
        self.actionExit.setObjectName("actionExit")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon3)
        self.actionUndo.setObjectName("actionUndo")
        self.actionErase = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/eraser.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionErase.setIcon(icon4)
        self.actionErase.setObjectName("actionErase")
        self.action3px = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/three.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action3px.setIcon(icon5)
        self.action3px.setObjectName("action3px")
        self.action5px = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/five.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action5px.setIcon(icon6)
        self.action5px.setObjectName("action5px")
        self.action7px = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/seven.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action7px.setIcon(icon7)
        self.action7px.setObjectName("action7px")
        self.action9px = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/nine.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action9px.setIcon(icon8)
        self.action9px.setObjectName("action9px")
        self.action11px = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/eleven.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action11px.setIcon(icon9)
        self.action11px.setObjectName("action11px")
        self.action13px = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/thirteen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action13px.setIcon(icon10)
        self.action13px.setObjectName("action13px")
        self.actionBlack = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/images/black.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBlack.setIcon(icon11)
        self.actionBlack.setObjectName("actionBlack")
        self.actionBlue = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/images/blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBlue.setIcon(icon12)
        self.actionBlue.setObjectName("actionBlue")
        self.actionRed = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/images/red.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRed.setIcon(icon13)
        self.actionRed.setObjectName("actionRed")
        self.actionYellow = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/images/yellow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionYellow.setIcon(icon14)
        self.actionYellow.setObjectName("actionYellow")
        self.actionGreen = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/images/green.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGreen.setIcon(icon15)
        self.actionGreen.setObjectName("actionGreen")
        self.actionSolid = QtWidgets.QAction(MainWindow)
        self.actionSolid.setObjectName("actionSolid")
        self.actionAir = QtWidgets.QAction(MainWindow)
        self.actionAir.setObjectName("actionAir")
        self.actionCalligraphy = QtWidgets.QAction(MainWindow)
        self.actionCalligraphy.setObjectName("actionCalligraphy")
        self.actionOil = QtWidgets.QAction(MainWindow)
        self.actionOil.setObjectName("actionOil")
        self.actionCrayon = QtWidgets.QAction(MainWindow)
        self.actionCrayon.setObjectName("actionCrayon")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClear)
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionErase)
        self.menuBrushSize.addAction(self.action3px)
        self.menuBrushSize.addAction(self.action5px)
        self.menuBrushSize.addAction(self.action7px)
        self.menuBrushSize.addAction(self.action9px)
        self.menuBrushSize.addAction(self.action11px)
        self.menuBrushSize.addAction(self.action13px)
        self.menuBrushColor.addAction(self.actionBlack)
        self.menuBrushColor.addAction(self.actionBlue)
        self.menuBrushColor.addAction(self.actionRed)
        self.menuBrushColor.addAction(self.actionYellow)
        self.menuBrushColor.addAction(self.actionGreen)
        self.menuBrushes.addAction(self.actionSolid)
        self.menuBrushes.addAction(self.actionAir)
        self.menuBrushes.addAction(self.actionCalligraphy)
        self.menuBrushes.addAction(self.actionOil)
        self.menuBrushes.addAction(self.actionCrayon)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuBrushSize.menuAction())
        self.menubar.addAction(self.menuBrushColor.menuAction())
        self.menubar.addAction(self.menuBrushes.menuAction())
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addAction(self.actionUndo)
        self.toolBar.addAction(self.actionErase)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuBrushSize.setTitle(_translate("MainWindow", "BrushSize"))
        self.menuBrushColor.setTitle(_translate("MainWindow", "BrushColor"))
        self.menuBrushes.setTitle(_translate("MainWindow", "Brushes"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionClear.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.actionErase.setText(_translate("MainWindow", "Erase"))
        self.actionErase.setShortcut(_translate("MainWindow", "Backspace"))
        self.action3px.setText(_translate("MainWindow", "3px"))
        self.action3px.setShortcut(_translate("MainWindow", "Ctrl+3"))
        self.action5px.setText(_translate("MainWindow", "5px"))
        self.action5px.setShortcut(_translate("MainWindow", "Ctrl+5"))
        self.action7px.setText(_translate("MainWindow", "7px"))
        self.action7px.setShortcut(_translate("MainWindow", "Ctrl+7"))
        self.action9px.setText(_translate("MainWindow", "9px"))
        self.action9px.setShortcut(_translate("MainWindow", "Ctrl+9"))
        self.action11px.setText(_translate("MainWindow", "11px"))
        self.action13px.setText(_translate("MainWindow", "13px"))
        self.actionBlack.setText(_translate("MainWindow", "Black"))
        self.actionBlue.setText(_translate("MainWindow", "Blue"))
        self.actionRed.setText(_translate("MainWindow", "Red"))
        self.actionYellow.setText(_translate("MainWindow", "Yellow"))
        self.actionGreen.setText(_translate("MainWindow", "Green"))
        self.actionSolid.setText(_translate("MainWindow", "Solid Brush"))
        self.actionAir.setText(_translate("MainWindow", "Air Brush"))
        self.actionCalligraphy.setText(_translate("MainWindow", "Calligraphy Brush"))
        self.actionOil.setText(_translate("MainWindow", "Oil Brush"))
        self.actionCrayon.setText(_translate("MainWindow", "Crayon Brush"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
