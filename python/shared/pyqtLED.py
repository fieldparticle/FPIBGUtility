from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QVBoxLayout, QLabel,QTabWidget, QListWidget
from PyQt6.QtGui import QPixmap,QImage
# For alignment flags
from PyQt6.QtCore import Qt
class QtLed(QWidget):

    def __init__(self, color=None):

        self.ledIcon = QLabel()
        self.ledIcon.setObjectName('ledIcon')

        self.changeColor(color)

        QWidget.__init__(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.ledIcon)

        self.ledIcon.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.ledIcon.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)

    def changeColor(self, color):

        pixmap = QPixmap('offLED.png')
        if color == "green":
            pixmap = QPixmap('greenLED.png')
        if color == "red":
            pixmap = QPixmap('redLED.png')
        pixmap = pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)

        self.ledIcon.setPixmap(pixmap)
