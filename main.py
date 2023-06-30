from paintWindow import Window
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys

app = QApplication(sys.argv)
window = Window(app)
window.show()
sys.exit(app.exec_())
