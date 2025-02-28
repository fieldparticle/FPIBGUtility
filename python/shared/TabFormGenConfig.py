import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt
import datetime


class TabGenConfig(QTabWidget):
    """ Object for the General Configuration Tab. This contains a form which allows the user to enter the specifications they would like to use for the simulation. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self):
        """ Constructor for the TabGenConfig object, which sets up the form on the tab. """
        ## Set up a layout object
        layout = QFormLayout()

        # Create the line edit for the folder path, with a button to browse
        self.folderLineEdit = QLineEdit()
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.browseFolder)
        # Add the folder line edit and the browse button to an HBox 
        hbox = QHBoxLayout()
        hbox.addWidget(self.folderLineEdit)
        hbox.addWidget(self.browseButton)
        # Add that HBox to the layout
        layout.addRow("Folder:", hbox)

        # Create a submit button
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.sendFormData)
        # Add that button to the layout
        layout.addWidget(self.submitButton)

        
        self.setLayout(layout)
    
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folderLineEdit.setText(folder)
            self.log_action("browseFolder", folder)
    
    def sendFormData(self):
        """ Sends data from the form to the config file writer """
        # TODO: Once this form is done, call the config file writer
        self.log_action("sendFormData", self.folderLineEdit.text())
        return self.folderLineEdit.text()

    def log_action(self, action, result):
        """ Log an action that is taken and the result of that action. """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("BRLogging.log", "a") as log:
                log.write(f"{timestamp} - action: {action}\n")
                log.write(f"{timestamp} - result: {result}\n")
        except Exception as e:
            print("Could not log")