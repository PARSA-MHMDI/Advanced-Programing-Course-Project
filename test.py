from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPixmap
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create a QGraphicsView
    view = QGraphicsView()

    view.setGeometry()

    # Create a QGraphicsScene
    scene = QGraphicsScene()

    # Load the image using QPixmap
    pixmap = QPixmap("./images/clear.jpg")

    # Create a QGraphicsPixmapItem with the loaded pixmap
    pixmap_item = scene.addPixmap(pixmap)

    # Add the pixmap item to the scene
    scene.addItem(pixmap_item)

    # Set the scene on the view
    view.setScene(scene)

    # Show the view
    view.show()

    sys.exit(app.exec_())
