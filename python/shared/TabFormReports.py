import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QWidget, QVBoxLayout,
    QTabWidget, QLabel, QScrollArea, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout )
from PyQt6.QtCore import Qt

class TabReports(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        main_layout = QVBoxLayout(scroll_widget)

        folder_group = QGroupBox("Folder Selection")
        folder_layout = QFormLayout()
        # Create folder selection row
        self.folderLineEdit = QLineEdit()
        self.browseButton = QPushButton("Browse")
        # Add the folder line edit and the browse button to an HBox
        hbox = QHBoxLayout()
        hbox.addWidget(self.folderLineEdit)
        hbox.addWidget(self.browseButton)
        # Add that HBox to the layout
        folder_label = QLabel("Folder Selection")
        # folder_layout.addRow("Folder:", hbox)
        folder_layout.addRow(folder_label, hbox)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)

        scroll_area.setWidget(scroll_widget)
        main_window_layout = QVBoxLayout(self)
        main_window_layout.addWidget(scroll_area)
        self.setLayout(main_window_layout)