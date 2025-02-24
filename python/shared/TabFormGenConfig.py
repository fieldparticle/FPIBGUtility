import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton
from PyQt6.QtCore import Qt

class TabGenConfig(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self):
        # personal page
        personal_page = QWidget(self)
        layout = QFormLayout()
        personal_page.setLayout(layout)
        layout.addRow('First Name:', QLineEdit(self))
        layout.addRow('Last Name:', QLineEdit(self))
        layout.addRow('DOB:', QDateEdit(self))
        self.addTab(personal_page, 'Personal Info')