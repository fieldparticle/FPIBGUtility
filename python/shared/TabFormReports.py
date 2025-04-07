import sys
from FPIBGPlotData import *
from FPIBGBase import *
import getpass 
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QWidget, QVBoxLayout,
    QTabWidget, QLabel, QScrollArea, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout,QRadioButton, QFileDialog, QSpacerItem, QSizePolicy, QTextEdit )
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

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
        guser = getpass.getuser() 
        bc = FPIBGBase("GlobalBaseClass")
        match guser:
            case "jbwk":
                bc.Create("ParticleJB.cfg",'MyLog.log')
            case _:
                bc.Create("ParticleKM.cfg",'KMLog.log')
        myClass = PlotData("ExampleObject")
        myClass.Create(bc,"PQB")
        myClass.Open()

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

        spfvn_image = QLabel()
        spfvn_pixmap = myClass.plot_B1()
        spfvn_image.setPixmap(spfvn_pixmap)

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
        
        table001_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        table001_buttons = QHBoxLayout()
        self.save_latex_table001_button = QPushButton("Save Latex")
        self.save_latex_table001_button.clicked.connect(lambda: self.save_latex(table001_image))
        self.save_latex_table001_button.setMaximumWidth(150)
        table001_buttons.addItem(spacer)
        table001_buttons.addWidget(self.save_latex_table001_button)

        table001_caption_container = QHBoxLayout()
        table001_caption_label = QLabel("Caption:")
        table001_caption_container.addWidget(table001_caption_label)
        self.table001_text_edit = QTextEdit()
        self.table001_text_edit.setMaximumHeight(80)
        table001_caption_container.addWidget(self.table001_text_edit)

        table001_layout.addLayout(table001_buttons)
        table001_layout.addWidget(table001_image)
        table001_layout.addLayout(table001_caption_container)

        self.table001_tab.setLayout(table001_layout)
        self.pqb_subreports.addTab(self.table001_tab, "Table001")

        ####### Linearity Compute #######
        self.lincom_tab = QWidget()
        lincom_layout = QVBoxLayout(self.lincom_tab)

        lincom_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        lincom_buttons = QHBoxLayout()
        self.save_latex_lincom_button = QPushButton("Save Latex")
        self.save_latex_lincom_button.clicked.connect(lambda: self.save_latex(lincom_image))
        self.save_latex_lincom_button.setMaximumWidth(150)
        self.save_image_lincom_button = QPushButton("Save Image")
        self.save_image_lincom_button.clicked.connect(lambda: self.save_image(lincom_image))
        self.save_image_lincom_button.setMaximumWidth(150)
        lincom_buttons.addItem(spacer)
        lincom_buttons.addWidget(self.save_latex_lincom_button)
        lincom_buttons.addWidget(self.save_image_lincom_button)

        lincom_caption_container = QHBoxLayout()
        lincom_caption_label = QLabel("Caption:")
        lincom_caption_container.addWidget(lincom_caption_label)
        self.lincom_text_edit = QTextEdit()
        self.lincom_text_edit.setMaximumHeight(80)
        lincom_caption_container.addWidget(self.lincom_text_edit)

        lincom_layout.addLayout(lincom_buttons)
        lincom_layout.addWidget(lincom_image)
        lincom_layout.addLayout(lincom_caption_container)

        self.lincom_tab.setLayout(lincom_layout)
        self.pqb_subreports.addTab(self.lincom_tab, "Linearity Compute")

        ####### Linearity Graphics #######
        self.lingraph_tab = QWidget()
        lingraph_layout = QVBoxLayout(self.lingraph_tab)

        lingraph_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        lingraph_buttons = QHBoxLayout()
        self.save_latex_lingraph_button = QPushButton("Save Latex")
        self.save_latex_lingraph_button.clicked.connect(lambda: self.save_latex(lingraph_image))
        self.save_latex_lingraph_button.setMaximumWidth(150)
        self.save_image_lingraph_button = QPushButton("Save Image")
        self.save_image_lingraph_button.clicked.connect(lambda: self.save_image(lingraph_image))
        self.save_image_lingraph_button.setMaximumWidth(150)
        lingraph_buttons.addItem(spacer)
        lingraph_buttons.addWidget(self.save_latex_lingraph_button)
        lingraph_buttons.addWidget(self.save_image_lingraph_button)

        lingraph_caption_container = QHBoxLayout()
        lingraph_caption_label = QLabel("Caption:")
        lingraph_caption_container.addWidget(lingraph_caption_label)
        self.lingraph_text_edit = QTextEdit()
        self.lingraph_text_edit.setMaximumHeight(80)
        lingraph_caption_container.addWidget(self.lingraph_text_edit)

        lingraph_layout.addLayout(lingraph_buttons)
        lingraph_layout.addWidget(lingraph_image)
        lingraph_layout.addLayout(lingraph_caption_container)

        self.lingraph_tab.setLayout(lingraph_layout)
        self.pqb_subreports.addTab(self.lingraph_tab, "Linearity Graphics")

        ####### Linearity Total #######
        self.lintot_tab = QWidget()
        lintot_layout = QVBoxLayout(self.lintot_tab)

        lintot_image = QLabel()
        lintot_pixmap = myClass.plot_linearity()
        lintot_image.setPixmap(lintot_pixmap)

        lintot_buttons = QHBoxLayout()
        self.save_latex_lintot_button = QPushButton("Save Latex")
        self.save_latex_lintot_button.clicked.connect(lambda: self.save_latex(lintot_image))
        self.save_latex_lintot_button.setMaximumWidth(150)
        self.save_image_lintot_button = QPushButton("Save Image")
        self.save_image_lintot_button.clicked.connect(lambda: self.save_image(lintot_image))
        self.save_image_lintot_button.setMaximumWidth(150)
        lintot_buttons.addItem(spacer)
        lintot_buttons.addWidget(self.save_latex_lintot_button)
        lintot_buttons.addWidget(self.save_image_lintot_button)

        lintot_caption_container = QHBoxLayout()
        lintot_caption_label = QLabel("Caption:")
        lintot_caption_container.addWidget(lintot_caption_label)
        self.lintot_text_edit = QTextEdit()
        self.lintot_text_edit.setMaximumHeight(80)
        lintot_caption_container.addWidget(self.lintot_text_edit)

        lintot_layout.addLayout(lintot_buttons)
        lintot_layout.addWidget(lintot_image)
        lintot_layout.addLayout(lintot_caption_container)

        self.lintot_tab.setLayout(lintot_layout)
        self.pqb_subreports.addTab(self.lintot_tab, "Linearity Total")

        ### Tab finishing
        pqb_layout.addWidget(self.save_latex_pqb_button)
        pqb_layout.addWidget(self.pqb_subreports)
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

        ####### SPf V Sidelength #######
        self.spfvside_tab = QWidget()
        spfvside_layout = QVBoxLayout(self.spfvside_tab)

        spfvside_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        spfvside_buttons = QHBoxLayout()
        self.save_latex_spfvside_button = QPushButton("Save Latex")
        self.save_latex_spfvside_button.clicked.connect(lambda: self.save_latex(spfvside_image))
        self.save_latex_spfvside_button.setMaximumWidth(150)
        self.save_image_spfvside_button = QPushButton("Save Image")
        self.save_image_spfvside_button.clicked.connect(lambda: self.save_image(spfvside_image))
        self.save_image_spfvside_button.setMaximumWidth(150)
        spfvside_buttons.addItem(spacer)
        spfvside_buttons.addWidget(self.save_latex_spfvside_button)
        spfvside_buttons.addWidget(self.save_image_spfvside_button)

        spfvside_caption_container = QHBoxLayout()
        spfvside_caption_label = QLabel("Caption:")
        spfvside_caption_container.addWidget(spfvside_caption_label)
        self.spfvside_text_edit = QTextEdit()
        self.spfvside_text_edit.setMaximumHeight(80)
        spfvside_caption_container.addWidget(self.spfvside_text_edit)

        spfvside_layout.addLayout(spfvside_buttons)
        spfvside_layout.addWidget(spfvside_image)
        spfvside_layout.addLayout(spfvside_caption_container)

        self.spfvside_tab.setLayout(spfvside_layout)
        self.pcd_subreports.addTab(self.spfvside_tab, "SPf V Sidelength")

        ### Tab finishing
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

        ####### SPf V Sidelength #######
        self.graphspfvn_tab = QWidget()
        graphspfvn_layout = QVBoxLayout(self.graphspfvn_tab)

        graphspfvn_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        graphspfvn_buttons = QHBoxLayout()
        self.save_latex_graphspfvn_button = QPushButton("Save Latex")
        self.save_latex_graphspfvn_button.clicked.connect(lambda: self.save_latex(graphspfvn_image))
        self.save_latex_graphspfvn_button.setMaximumWidth(150)
        self.save_image_graphspfvn_button = QPushButton("Save Image")
        self.save_image_graphspfvn_button.clicked.connect(lambda: self.save_image(graphspfvn_image))
        self.save_image_graphspfvn_button.setMaximumWidth(150)
        graphspfvn_buttons.addItem(spacer)
        graphspfvn_buttons.addWidget(self.save_latex_graphspfvn_button)
        graphspfvn_buttons.addWidget(self.save_image_graphspfvn_button)

        graphspfvn_caption_container = QHBoxLayout()
        graphspfvn_caption_label = QLabel("Caption:")
        graphspfvn_caption_container.addWidget(graphspfvn_caption_label)
        self.graphspfvn_text_edit = QTextEdit()
        self.graphspfvn_text_edit.setMaximumHeight(80)
        graphspfvn_caption_container.addWidget(self.graphspfvn_text_edit)

        graphspfvn_layout.addLayout(graphspfvn_buttons)
        graphspfvn_layout.addWidget(graphspfvn_image)
        graphspfvn_layout.addLayout(graphspfvn_caption_container)

        self.graphspfvn_tab.setLayout(graphspfvn_layout)
        self.cfb_subreports.addTab(self.graphspfvn_tab, "Graphics SPF v N")

        ####### SPf V Sidelength #######
        self.compspfvn_tab = QWidget()
        compspfvn_layout = QVBoxLayout(self.compspfvn_tab)

        compspfvn_image = QLabel("PLACEHOLDER WIDGET FOR IMAGE")

        compspfvn_buttons = QHBoxLayout()
        self.save_latex_compspfvn_button = QPushButton("Save Latex")
        self.save_latex_compspfvn_button.clicked.connect(lambda: self.save_latex(compspfvn_image))
        self.save_latex_compspfvn_button.setMaximumWidth(150)
        self.save_image_compspfvn_button = QPushButton("Save Image")
        self.save_image_compspfvn_button.clicked.connect(lambda: self.save_image(compspfvn_image))
        self.save_image_compspfvn_button.setMaximumWidth(150)
        compspfvn_buttons.addItem(spacer)
        compspfvn_buttons.addWidget(self.save_latex_compspfvn_button)
        compspfvn_buttons.addWidget(self.save_image_compspfvn_button)

        compspfvn_caption_container = QHBoxLayout()
        compspfvn_caption_label = QLabel("Caption:")
        compspfvn_caption_container.addWidget(compspfvn_caption_label)
        self.compspfvn_text_edit = QTextEdit()
        self.compspfvn_text_edit.setMaximumHeight(80)
        compspfvn_caption_container.addWidget(self.compspfvn_text_edit)

        compspfvn_layout.addLayout(compspfvn_buttons)
        compspfvn_layout.addWidget(compspfvn_image)
        compspfvn_layout.addLayout(compspfvn_caption_container)

        self.compspfvn_tab.setLayout(compspfvn_layout)
        self.cfb_subreports.addTab(self.compspfvn_tab, "Compute SPF v N")

        ### Tab finishing
        cfb_layout.addWidget(self.save_latex_cfb_button)
        cfb_layout.addWidget(self.cfb_subreports)
        self.cfb_tab.setLayout(cfb_layout)
        self.report_tabs.addTab(self.cfb_tab, "CFB")

        # Add the embedded tab widget to the main layout
        main_layout.addWidget(self.report_tabs)

        scroll_area.setWidget(scroll_widget)
        main_window_layout = QVBoxLayout(self)
        main_window_layout.addWidget(scroll_area)
        self.setLayout(main_window_layout)