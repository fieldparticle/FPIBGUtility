import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QWidget, QVBoxLayout,
    QTabWidget, QLabel, QScrollArea, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout,QRadioButton, QFileDialog, QSpacerItem, QSizePolicy, QTextEdit )
from PyQt6.QtCore import Qt

class TabReports(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def browseFolder(self):
        """ Opens a dialog window for the user to select a folder in the file system. """
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folderLineEdit.setText(folder)
            self.log_action("browseFolder", folder)

    def get_selected_mode(self):
        """ Function to get the selected mode: 1 for "Verify", 0 for "Performance", -1 for no selection """
        selected = None
        if self.verify_radio.isChecked():
            return 1
        elif self.perform_radio.isChecked():
            return 0
        else:
            return -1

    def get_output_dir(self):
        return self.folderLineEdit.text()

    def save_latex_pqb(self):
        #TODO
        return
    def save_latex_pcd(self):
        #TODO
        return
    def save_latex_cfb(self):
        #TODO
        return
    def save_latex_all(self):
        #TODO
        return
    def save_image(self, widget):
        #TODO
        return
    def save_latex(self, widget):
        #TODO
        return

    def Create(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        main_layout = QVBoxLayout(scroll_widget)

        group_box = QGroupBox("Report Options")
        form_layout = QFormLayout()

        #Directory Selection
        self.folderLineEdit = QLineEdit()
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.browseFolder)
        self.save_latex_all_button = QPushButton("Save Latex All")
        self.save_latex_all_button.clicked.connect(self.save_latex_all)
        folder_label = QLabel("Output Directory")
        hbox = QHBoxLayout()
        hbox.addWidget(folder_label)
        hbox.addWidget(self.folderLineEdit)
        hbox.addWidget(self.browseButton)
        hbox.addWidget(self.save_latex_all_button)

        #Mode Selection
        self.options_group = QGroupBox("Mode")
        self.options_layout = QVBoxLayout()
        self.verify_radio = QRadioButton("Verify (D)")
        self.perform_radio = QRadioButton("Performance (R)")
        self.options_layout.addWidget(self.verify_radio)
        self.options_layout.addWidget(self.perform_radio)
        self.options_group.setLayout(self.options_layout)

        form_layout.addRow(self.options_group, hbox)
        # form_layout.addRow(hbox)
        group_box.setLayout(form_layout)
        
        main_layout.addWidget(group_box)

        # --- Embedded QTabWidget for reports ---
        self.report_tabs = QTabWidget()

        #########################
        #### PQB REPORT TABS ####
        #########################
        self.pqb_tab = QWidget()
        pqb_layout = QVBoxLayout(self.pqb_tab)
        self.save_latex_pqb_button = QPushButton("Save Latex PQB")
        self.save_latex_pqb_button.clicked.connect(self.save_latex_pqb)
        self.save_latex_pqb_button.setMaximumWidth(150)
        self.pqb_subreports = QTabWidget()

        ####### FPS v N #######
        self.fpsvn_tab = QWidget()
        fpsvn_layout = QVBoxLayout(self.fpsvn_tab)
        
        fpsvn_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        fpsvn_buttons = QHBoxLayout()
        spacer = QSpacerItem(40, 2, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.save_latex_fpsvn_button = QPushButton("Save Latex")
        self.save_latex_fpsvn_button.clicked.connect(lambda: self.save_latex(fpsvn_image))
        self.save_latex_fpsvn_button.setMaximumWidth(150)
        self.save_image_fpsvn_button = QPushButton("Save Image")
        self.save_image_fpsvn_button.clicked.connect(lambda: self.save_image(fpsvn_image))
        self.save_image_fpsvn_button.setMaximumWidth(150)
        fpsvn_buttons.addItem(spacer)
        fpsvn_buttons.addWidget(self.save_latex_fpsvn_button)
        fpsvn_buttons.addWidget(self.save_image_fpsvn_button)

        fpsvn_caption_container = QHBoxLayout()
        fpsvn_caption_label = QLabel("Caption:")
        fpsvn_caption_container.addWidget(fpsvn_caption_label)
        self.fpsvn_text_edit = QTextEdit()
        self.fpsvn_text_edit.setMaximumHeight(80)
        fpsvn_caption_container.addWidget(self.fpsvn_text_edit)
        
        fpsvn_layout.addLayout(fpsvn_buttons)
        fpsvn_layout.addWidget(fpsvn_image)
        fpsvn_layout.addLayout(fpsvn_caption_container)
        
        self.fpsvn_tab.setLayout(fpsvn_layout)
        self.pqb_subreports.addTab(self.fpsvn_tab, "FPS v N")

        ####### SPF v N #######
        self.spfvn_tab = QWidget()
        spfvn_layout = QVBoxLayout(self.spfvn_tab)

        spfvn_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        spfvn_buttons = QHBoxLayout()
        self.save_latex_spfvn_button = QPushButton("Save Latex")
        self.save_latex_spfvn_button.clicked.connect(lambda: self.save_latex(spfvn_image))
        self.save_latex_spfvn_button.setMaximumWidth(150)
        self.save_image_spfvn_button = QPushButton("Save Image")
        self.save_image_spfvn_button.clicked.connect(lambda: self.save_image(spfvn_image))
        self.save_image_spfvn_button.setMaximumWidth(150)
        spfvn_buttons.addItem(spacer)
        spfvn_buttons.addWidget(self.save_latex_spfvn_button)
        spfvn_buttons.addWidget(self.save_image_spfvn_button)

        spfvn_caption_container = QHBoxLayout()
        spfvn_caption_label = QLabel("Caption:")
        spfvn_caption_container.addWidget(spfvn_caption_label)
        self.spfvn_text_edit = QTextEdit()
        self.spfvn_text_edit.setMaximumHeight(80)
        spfvn_caption_container.addWidget(self.spfvn_text_edit)

        spfvn_layout.addLayout(spfvn_buttons)
        spfvn_layout.addWidget(spfvn_image)
        spfvn_layout.addLayout(spfvn_caption_container)

        self.spfvn_tab.setLayout(spfvn_layout)
        self.pqb_subreports.addTab(self.spfvn_tab, "SPF v N")

        ####### Table001 #######
        self.table001_tab = QWidget()
        table001_layout = QVBoxLayout(self.table001_tab)
        
        spfvn_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        spfvn_buttons = QHBoxLayout()
        self.save_latex_spfvn_button = QPushButton("Save Latex")
        self.save_latex_spfvn_button.clicked.connect(lambda: self.save_latex(spfvn_image))
        self.save_latex_spfvn_button.setMaximumWidth(150)
        self.save_image_spfvn_button = QPushButton("Save Image")
        self.save_image_spfvn_button.clicked.connect(lambda: self.save_image(spfvn_image))
        self.save_image_spfvn_button.setMaximumWidth(150)
        spfvn_buttons.addItem(spacer)
        spfvn_buttons.addWidget(self.save_latex_spfvn_button)
        spfvn_buttons.addWidget(self.save_image_spfvn_button)

        spfvn_caption_container = QHBoxLayout()
        spfvn_caption_label = QLabel("Caption:")
        spfvn_caption_container.addWidget(spfvn_caption_label)
        self.spfvn_text_edit = QTextEdit()
        self.spfvn_text_edit.setMaximumHeight(80)
        spfvn_caption_container.addWidget(self.spfvn_text_edit)

        spfvn_layout.addLayout(spfvn_buttons)
        spfvn_layout.addWidget(spfvn_image)
        spfvn_layout.addLayout(spfvn_caption_container)

        self.table001_tab.setLayout(table001_layout)
        self.pqb_subreports.addTab(self.table001_tab, "Table001")

        self.lincom_tab = QWidget()
        lincom_layout = QVBoxLayout(self.lincom_tab)
        #TODO: Insert Linearity Compute content here
        #END Linearity Compute content
        self.lincom_tab.setLayout(lincom_layout)
        self.pqb_subreports.addTab(self.lincom_tab, "Linearity Compute")

        self.lingraph_tab = QWidget()
        lingraph_layout = QVBoxLayout(self.lingraph_tab)
        #TODO: Insert Linearity Graphics content here
        #END Linearity Graphics content
        self.lingraph_tab.setLayout(lingraph_layout)
        self.pqb_subreports.addTab(self.lingraph_tab, "Linearity Graphics")

        self.lintot_tab = QWidget()
        lintot_layout = QVBoxLayout(self.lintot_tab)
        #TODO: Insert Linearity Total content here
        #END Linearity Total content
        self.lintot_tab.setLayout(lintot_layout)
        self.pqb_subreports.addTab(self.lintot_tab, "Linearity Total")

        pqb_layout.addWidget(self.save_latex_pqb_button)
        pqb_layout.addWidget(self.pqb_subreports)
        # pqb_layout.addWidget(label1)
        self.pqb_tab.setLayout(pqb_layout)
        self.report_tabs.addTab(self.pqb_tab, "PQB")

        #########################
        #### PCD REPORT TABS ####
        #########################
        self.pcd_tab = QWidget()
        pcd_layout = QVBoxLayout(self.pcd_tab)
        self.save_latex_pcd_button = QPushButton("Save Latex PCD")
        self.save_latex_pcd_button.clicked.connect(self.save_latex_pcd)
        self.save_latex_pcd_button.setMaximumWidth(150)
        self.pcd_subreports = QTabWidget()

        self.spfvside_tab = QWidget()
        spfvside_layout = QVBoxLayout(self.spfvside_tab)
        #TODO: Insert fpsvn content here
        #END fpsvn content
        self.spfvside_tab.setLayout(spfvside_layout)
        self.pcd_subreports.addTab(self.spfvside_tab, "SPf V Sidelength")

        pcd_layout.addWidget(self.save_latex_pcd_button)
        pcd_layout.addWidget(self.pcd_subreports)
        self.pcd_tab.setLayout(pcd_layout)
        self.report_tabs.addTab(self.pcd_tab, "PCD")

        #########################
        #### CFB REPORT TABS ####
        #########################
        self.cfb_tab = QWidget()
        cfb_layout = QVBoxLayout(self.cfb_tab)
        self.save_latex_cfb_button = QPushButton("Save Latex CFB")
        self.save_latex_cfb_button.clicked.connect(self.save_latex_cfb)
        self.save_latex_cfb_button.setMaximumWidth(150)
        self.cfb_subreports = QTabWidget()

        self.graphspfvn_tab = QWidget()
        graphspfvn_layout = QVBoxLayout(self.graphspfvn_tab)
        #TODO: Insert fpsvn content here
        #END fpsvn content
        self.graphspfvn_tab.setLayout(graphspfvn_layout)
        self.cfb_subreports.addTab(self.graphspfvn_tab, "Graphics SPF v N")

        self.compspfvn_tab = QWidget()
        compspfvn_layout = QVBoxLayout(self.compspfvn_tab)
        #TODO: Insert fpsvn content here
        #END fpsvn content
        self.compspfvn_tab.setLayout(compspfvn_layout)
        self.cfb_subreports.addTab(self.compspfvn_tab, "Compute SPF v N")

        cfb_layout.addWidget(self.save_latex_cfb_button)
        cfb_layout.addWidget(self.cfb_subreports)
        # cfb_layout.addWidget(label2)
        self.cfb_tab.setLayout(cfb_layout)
        self.report_tabs.addTab(self.cfb_tab, "CFB")

        # Add the embedded tab widget to the main layout
        main_layout.addWidget(self.report_tabs)

        scroll_area.setWidget(scroll_widget)
        main_window_layout = QVBoxLayout(self)
        main_window_layout.addWidget(scroll_area)
        self.setLayout(main_window_layout)