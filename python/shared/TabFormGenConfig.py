import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt


class TabGenConfig(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self):
        ## Set up a layout object
        layout = QFormLayout()

        self.folderLineEdit = QLineEdit()
        self.browseButton = QPushButton("Browse")

        hbox = QHBoxLayout()
        hbox.addWidget(self.folderLineEdit)
        hbox.addWidget(self.browseButton)

        layout.addRow("Folder:", hbox)

        self.browseButton.clicked.connect(self.browseFolder)
        self.setLayout(layout)
    
    def browseFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folderLineEdit.setText(folder)