from paintWindow import Window
from PyQt5.QtWidgets import QApplication
import sys

app=QApplication(sys.argv)
window=Window(app)
window.show()
sys.exit(app.exec())