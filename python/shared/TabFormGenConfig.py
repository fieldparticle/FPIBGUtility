import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QFormLayout, QGridLayout, QTabWidget, QLineEdit, QDateEdit, QPushButton, QLabel, QHBoxLayout, QFileDialog, QVBoxLayout, QGroupBox, QCheckBox, QSpinBox
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt
import datetime


class TabGenConfig(QTabWidget):
    """ Object for the General Configuration Tab. This contains a form which allows the user to enter the specifications they would like to use for the simulation. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def Create(self):
        """ Constructor for the TabGenConfig object, which sets up the form on the tab. """
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
        #Do Auto (checkbox)
        self.doauto_checkbox = QCheckBox()
        doauto_label = QLabel("Do Auto")
        flow_layout.addRow(self.doauto_checkbox, doauto_label)
        #Do Auto Wait (checkbox)
        self.doautowait_checkbox = QCheckBox()
        doautowait_label = QLabel("Do Auto Wait")
        flow_layout.addRow(self.doautowait_checkbox, doautowait_label)
        #Stop on data (checkbox)
        self.stop_on_data_checkbox = QCheckBox()
        stop_on_data_label = QLabel("Stop On Data")
        flow_layout.addRow(self.stop_on_data_checkbox, stop_on_data_label)
        #Stop on data (checkbox)
        self.no_compute_checkbox = QCheckBox()
        no_compute_label = QLabel("No Compute")
        flow_layout.addRow(self.no_compute_checkbox, no_compute_label)
        #Debug level (int)
        self.debug_level = QSpinBox()
        debug_level_label = QLabel("Debug Level")
        flow_layout.addRow(self.debug_level, debug_level_label)
        #Report Compute Frames (int)
        self.report_compute_frames = QLineEdit()
        frame_validator = QIntValidator()
        frame_validator.setRange(0, 1000000)
        self.report_compute_frames.setValidator(frame_validator)
        report_compute_frames_label = QLabel("Report Compute Frames")
        flow_layout.addRow(self.report_compute_frames, report_compute_frames_label)
        #Report Graphics Frames (int)
        self.report_graphics_frames = QLineEdit()
        self.report_graphics_frames.setValidator(frame_validator)
        report_graphics_frames_label = QLabel("Report Graphics Frames")
        flow_layout.addRow(self.report_graphics_frames, report_graphics_frames_label)

        flow_group.setLayout(flow_layout)
        main_layout.addWidget(flow_group)

        ### SECTION 3: GPU ###
        gpu_group = QGroupBox("GPU")
        gpu_layout = QFormLayout()
        # GPU Model (string)
        self.gpu_model = QLineEdit()
        gpu_model_label = QLabel("GPU Model")
        gpu_layout.addRow(self.gpu_model, gpu_model_label)
        # Frame Delay (int)
        self.frame_delay = QLineEdit()
        self.frame_delay.setValidator(frame_validator)
        frame_delay_label = QLabel("Frame Delay")
        gpu_layout.addRow(self.frame_delay,  frame_delay_label)
        # End Frame (int)
        self.end_frame = QLineEdit()
        self.end_frame.setValidator(frame_validator)
        end_frame_label = QLabel("End Frame")
        gpu_layout.addRow(self.end_frame,  end_frame_label)
        # dt (int)
        self.dt = QLineEdit()
        self.dt.setValidator(frame_validator)
        dt_label = QLabel("dt")
        gpu_layout.addRow(self.dt, dt_label)
        # Compile Shaders (checkbox)
        self.compile_shaders_checkbox = QCheckBox()
        compile_shaders_label = QLabel("Compile Shaders")
        gpu_layout.addRow(compile_shaders_label, self.compile_shaders_checkbox)
        # Fragment Kernel (browse file)
        self.frag_kernel = QLineEdit()
        self.frag_browseButton = QPushButton("Browse")
        self.frag_browseButton.clicked.connect(self.browseFileFrag)
        frag_hbox = QHBoxLayout()
        frag_hbox.addWidget(self.frag_kernel)
        frag_hbox.addWidget(self.frag_browseButton)
        gpu_layout.addRow("Fragment Kernel:", frag_hbox)
        # Vertex Kernel (browse file)
        self.vert_kernel = QLineEdit()
        self.vert_browseButton = QPushButton("Browse")
        self.vert_browseButton.clicked.connect(self.browseFileVert)
        vert_hbox = QHBoxLayout()
        vert_hbox.addWidget(self.vert_kernel)
        vert_hbox.addWidget(self.vert_browseButton)
        gpu_layout.addRow("Vertex Kernel:", vert_hbox)
        # Compute Kernel (browse file)
        self.comp_kernel = QLineEdit()
        self.comp_browseButton = QPushButton("Browse")
        self.comp_browseButton.clicked.connect(self.browseFileComp)
        comp_hbox = QHBoxLayout()
        comp_hbox.addWidget(self.comp_kernel)
        comp_hbox.addWidget(self.comp_browseButton)
        gpu_layout.addRow("Compute Kernel:", comp_hbox)

        gpu_group.setLayout(gpu_layout)
        main_layout.addWidget(gpu_group)

        ### SECTION 4: LAUNCH ###
        launch_group = QGroupBox("Launch")
        launch_layout = QFormLayout()
        # Report Extensions (checkbox)
        self.rep_ext_checkbox = QCheckBox()
        rep_ext_label = QLabel("Report Extensions")
        launch_layout.addRow(self.rep_ext_checkbox, rep_ext_label)
        # Report Device Limits (checkbox)
        self.rep_lim_checkbox = QCheckBox()
        rep_lim_label = QLabel("Report Device Limitations")
        launch_layout.addRow(self.rep_lim_checkbox, rep_lim_label)
        # Enable Validation Layers (checkbox)
        self.val_layers_checkbox = QCheckBox()
        val_layers_label = QLabel("Enable Validation Layers")
        launch_layout.addRow(self.val_layers_checkbox, val_layers_label)
        # TODO: Device Extensions, Instance Extensions, Validation Layers: These are lists of strings that you can add to and remove from, and should be displayed

        launch_group.setLayout(launch_layout)
        main_layout.addWidget(launch_group)


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
    
    def browseFileFrag(self):
        """ Opens a dialog window for the user to select a file in the file system for the frag kernel. """
        file = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            self.frag_kernel.setText(file[0])
            self.log_action("browseFile", file[0])
    
    def browseFileVert(self):
        """ Opens a dialog window for the user to select a file in the file system for the vertex kernel. """
        file = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            self.vert_kernel.setText(file[0])
            self.log_action("browseFile", file[0])
    
    def browseFileComp(self):
        """ Opens a dialog window for the user to select a file in the file system for the compute kernel. """
        file = QFileDialog.getOpenFileName(self, "Select File")
        if file:
            self.comp_kernel.setText(file[0])
            self.log_action("browseFile", file[0])

    def sendFormData(self):
        """ Sends data from the form to the config file writer """
        # TODO: Once this form is done, call the config file writer

        config_dict = {}
        # Add section 1 details
        config_dict["folder"] = self.folderLineEdit.text()
        # Add section 2 details
        config_dict["do_auto"] = self.doauto_checkbox.isChecked()
        config_dict["do_auto_wait"] = self.doautowait_checkbox.isChecked()
        config_dict["stop_on_data"] = self.stop_on_data_checkbox.isChecked()
        config_dict["no_compute"] = self.no_compute_checkbox.isChecked()
        config_dict["debug_level"] = self.debug_level.value()
        config_dict["report_compute_frames"] = self.report_compute_frames.text()
        config_dict["report_graphics_frames"] = self.report_graphics_frames.text()
        # Add Section 3 Details
        config_dict["gpu_model"] = self.gpu_model.text()
        config_dict["frame_delay"] = self.frame_delay.value()
        config_dict["end_frame"] = self.end_frame.value()
        config_dict["dt"] = self.dt.value()
        config_dict["compile_shaders"] = self.compile_shaders_checkbox.isChecked()
        config_dict["frag_kernel"] = self.frag_kernel.text()
        config_dict["vert_kernel"] = self.vert_kernel.text()
        config_dict["comp_kernel"] = self.comp_kernel.text()
        # Add section 4 details
        config_dict["rep_ext"] = self.rep_ext_checkbox.isChecked()
        config_dict["rep_lim"] = self.rep_lim_checkbox.isChecked()
        config_dict["val_layers"] = self.val_layers_checkbox.isChecked()

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