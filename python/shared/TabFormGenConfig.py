import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QVBoxLayout, QGroupBox, QCheckBox
from PyQt6.QtCore import Qt
import datetime


class TabGenConfig(QTabWidget):
    """ Object for the General Configuration Tab. This contains a form which allows the user to enter the specifications they would like to use for the simulation. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self):
        """ Constructor for the TabGenConfig object, which sets up the form on the tab. """
        # ## Set up a layout object
        # layout = QFormLayout()

        # ## FOLDER SELECTION ##
        # self.folderLineEdit = QLineEdit()
        # self.browseButton = QPushButton("Browse")
        # self.browseButton.clicked.connect(self.browseFolder)
        # # Add the folder line edit and the browse button to an HBox 
        # hbox = QHBoxLayout()
        # hbox.addWidget(self.folderLineEdit)
        # hbox.addWidget(self.browseButton)
        # # Add that HBox to the layout
        # layout.addRow("Folder:", hbox)



        # ## SUBMIT BUTTON ##
        # self.submitButton = QPushButton("Submit")
        # self.submitButton.clicked.connect(self.sendFormData)
        # # Add that button to the layout
        # layout.addWidget(self.submitButton)

        
        # self.setLayout(layout)


        main_layout = QVBoxLayout()

        ### SECTION 1: FOLDER SELECTION ###
        folder_group = QGroupBox("Folder Selection")
        folder_layout = QFormLayout()
        # Create folder selection row
        self.folderLineEdit = QLineEdit()
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.browseFolder)
        # Add the folder line edit and the browse button to an HBox 
        hbox = QHBoxLayout()
        hbox.addWidget(self.folderLineEdit)
        hbox.addWidget(self.browseButton)
        # Add that HBox to the layout
        folder_layout.addRow("Folder:", hbox)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)

        ### SECTION 2: FLOW CONTROL ###
        flow_group = QGroupBox("Flow Control")
        flow_layout = QFormLayout()
        #Do Auto
        self.doauto_checkbox = QCheckBox()
        doauto_label = QLabel("Do Auto")
        flow_layout.addRow(self.doauto_checkbox, doauto_label)
        #Do Auto Wait
        self.doautowait_checkbox = QCheckBox()
        doautowait_label = QLabel("Do Auto Wait")
        flow_layout.addRow(self.doautowait_checkbox, doautowait_label)

        email_label = QLabel("Email:")
        email_edit = QLineEdit()
        flow_layout.addRow(email_label, email_edit)

        phone_label = QLabel("Phone:")
        phone_edit = QLineEdit()
        flow_layout.addRow(phone_label, phone_edit)

        flow_group.setLayout(flow_layout)
        main_layout.addWidget(flow_group)

        ## SUBMIT BUTTON ##
        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.sendFormData)
        # Add that button to the layout
        main_layout.addWidget(self.submitButton)

        self.setLayout(main_layout)
    
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folderLineEdit.setText(folder)
            self.log_action("browseFolder", folder)
    
    def sendFormData(self):
        """ Sends data from the form to the config file writer """
        # TODO: Once this form is done, call the config file writer

        config_dict = {}
        config_dict["folder"] = self.folderLineEdit.text()
        config_dict["do_auto"] = self.doauto_checkbox.isChecked()
        config_dict["do_auto_wait"] = self.doautowait_checkbox.isChecked()

        self.log_action("sendFormData", config_dict)
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