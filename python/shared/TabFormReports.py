import sys
from FPIBGPlotData import *
from FPIBGBase import *
import getpass 
from LatexClass import *
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QWidget, QVBoxLayout,
    QTabWidget, QLabel, QScrollArea, QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout,QRadioButton, QFileDialog, QSpacerItem, QSizePolicy, QTextEdit,QTableView )
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from FPIBGData import *
from TableModel import *

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

    def updateData(self):
        self.data = DataClass("DataClass")
        self.data.Create(self.bobj)
        self.data.Open("PQB")
        if (self.data.check_data_files() != True):
            print("Did not work") 
        self.data.create_summary()
        self.data.get_averages()

        self.dataPlot = PlotData("Data Plot Class")
        self.dataPlot.Create(self.bobj)
        self.dataPlot.Open("PQB","r")
       

        if(self.dataPlot.hasData() == True):
            fpsvn_pixmap = self.dataPlot.PlotData("fpsvn")
            self.fpsvn_image.setPixmap(fpsvn_pixmap)

            spfvn_pixmap = self.dataPlot.PlotData("spfvn")
            self.spfvn_image.setPixmap(spfvn_pixmap)

            lintot_pixmap = self.dataPlot.PlotData("lintot")
            self.lintot_image.setPixmap(lintot_pixmap)

            spfvside_pixmap = self.dataPlot.PlotData("spfvside")
            self.spfvside_image.setPixmap(spfvside_pixmap)
        
        self.dataPlot.Open("PCD","r")
        self.data.Open("PCD")
        if (self.data.check_data_files() != True):
            print("Did not work") 

        if(self.dataPlot.hasData() == True):
            spfvside_pixmap = self.dataPlot.PlotData("spfvside")
            self.spfvside_image.setPixmap(spfvside_pixmap)
            
        self.fpsvnltx = LatexPlot("LatexClass")
        self.fpsvnltx.Create(self.folderLineEdit.text(),"fpsvn")
        caption = self.fpsvnltx.readCapFile()
        self.fpsvn_text_edit.setText(caption)

        self.spfvnltx = LatexPlot("LatexClass")
        self.spfvnltx.Create(self.folderLineEdit.text(),"spfvn")
        caption = self.spfvnltx.readCapFile()
        self.spfvn_text_edit.setText(caption)

        ## Uodate Tables
        self.data.Open("PQB")
        header = self.data.query()
        latexFile = ["fps", "cpums", "cms", "gms", "loadedp"]
        
        tdata = self.data.return_table(latexFile)
        self.model = PandasModel(tdata)
        self.table001_image.setModel(self.model)
        self.table001_image.show()
        
        

    
    def get_output_dir(self):
        return self.folderLineEdit.text()

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    def save_latex_pqb(self):
        self.dataPlot.Open("PQB","r")
        if(self.dataPlot.hasData() == True):
            self.dataPlot.PlotData("fpsvn")
            self.dataPlot.fpsvnfig
            self.fpsvnltx = LatexPlot("LatexClass")
            self.fpsvnltx.Create(self.folderLineEdit.text(),"fpsvn")
            self.fpsvnltx.caption =  self.fpsvn_text_edit.toPlainText()
            self.fpsvnltx.width = 0
            self.fpsvnltx.height = 0
            self.fpsvnltx.title = "TITLE:Plot of fps v loadedp"
            self.fpsvnltx.scale = 0.50
            self.fpsvnltx.fontSize = 10
            self.fpsvnltx.outDirectory = self.cfg.latex_dir
            self.fpsvnltx.float = False
            self.fpsvnltx.placement = "h"
            self.fpsvnltx.Write(plt)
       
       
       
        if(self.dataPlot.hasData() == True):
            self.dataPlot.PlotData("spfvn")
            self.fpsvnltx = LatexPlot("LatexClass")
            self.fpsvnltx.Create(self.folderLineEdit.text(),"spfvn")
            self.fpsvnltx.caption =  self.spfvn_text_edit.toPlainText()
            self.fpsvnltx.width = 0
            self.fpsvnltx.height = 0
            self.fpsvnltx.title = "TITLE:spf v loaded p"
            self.fpsvnltx.scale = 0.50
            self.fpsvnltx.fontSize = 10
            self.fpsvnltx.outDirectory = self.cfg.latex_dir
            self.fpsvnltx.float = False
            self.fpsvnltx.placement = "h"
            self.fpsvnltx.Write(self.dataPlot.spfvnfig)
            
      
    def save_latex_pcd(self):
        print("pqb")
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
        
        ## Latex stuff
        latxheader = ["FPS","CPU Time(ms)","Commpute Time(ms)","Graphics Time(ms)","Number particles"]
        self.model.Latex.setLatexHeaderArray(latxheader)
        self.model.Latex.name = "perftable"
        self.model.Latex.WriteLatexTable()
        return

    def Create(self, FPIBGBase):
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.latexDir = self.cfg.latex_dir

     
        
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
        self.folderLineEdit.setText(self.latexDir)
        self.updateButton = QPushButton("Update Data")
        self.setSize(self.updateButton,30,150)
        self.updateButton.setStyleSheet("background-color:  #dddddd")
        hbox.addWidget(self.updateButton)
        self.updateButton.clicked.connect(self.updateData)

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

        self.fpsvn_image = QLabel()
       

        fpsvn_buttons = QHBoxLayout()
        spacer = QSpacerItem(40, 2, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.save_latex_fpsvn_button = QPushButton("Save Latex")
        self.save_latex_fpsvn_button.clicked.connect(lambda: self.save_latex(self.fpsvn_image))
        self.save_latex_fpsvn_button.setMaximumWidth(150)
        self.save_image_fpsvn_button = QPushButton("Save Image")
        self.save_image_fpsvn_button.clicked.connect(lambda: self.save_image(self.fpsvn_image))
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
        fpsvn_layout.addWidget(self.fpsvn_image)
        fpsvn_layout.addLayout(fpsvn_caption_container)
        
        self.fpsvn_tab.setLayout(fpsvn_layout)
        self.pqb_subreports.addTab(self.fpsvn_tab, "FPS v N")

        ####### SPF v N #######
        self.spfvn_tab = QWidget()
        spfvn_layout = QVBoxLayout(self.spfvn_tab)

        self.spfvn_image = QLabel()
       

        spfvn_buttons = QHBoxLayout()
        self.save_latex_spfvn_button = QPushButton("Save Latex")
        self.save_latex_spfvn_button.clicked.connect(lambda: self.save_latex(self.spfvn_image))
        self.save_latex_spfvn_button.setMaximumWidth(150)
        self.save_image_spfvn_button = QPushButton("Save Image")
        self.save_image_spfvn_button.clicked.connect(lambda: self.save_image(self.spfvn_image))
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
        spfvn_layout.addWidget(self.spfvn_image)
        spfvn_layout.addLayout(spfvn_caption_container)

        self.spfvn_tab.setLayout(spfvn_layout)
        self.pqb_subreports.addTab(self.spfvn_tab, "SPF v N")

        ####### Table001 #######
        self.table001_tab = QWidget()
        table001_layout = QVBoxLayout(self.table001_tab)
        
        self.table001_image = QTableView()

        table001_buttons = QHBoxLayout()
        self.save_latex_table001_button = QPushButton("Save Latex")
        self.save_latex_table001_button.clicked.connect(lambda: self.save_latex(self.table001_image))
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
        table001_layout.addWidget(self.table001_image)
        table001_layout.addLayout(table001_caption_container)

        self.table001_tab.setLayout(table001_layout)
        self.pqb_subreports.addTab(self.table001_tab, "Table001")

       
        ####### Linearity Total #######
        self.lintot_tab = QWidget()
        lintot_layout = QVBoxLayout(self.lintot_tab)

        self.lintot_image = QLabel()
      

        lintot_buttons = QHBoxLayout()
        self.save_latex_lintot_button = QPushButton("Save Latex")
        self.save_latex_lintot_button.clicked.connect(lambda: self.save_latex(self.lintot_image))
        self.save_latex_lintot_button.setMaximumWidth(150)
        self.save_image_lintot_button = QPushButton("Save Image")
        self.save_image_lintot_button.clicked.connect(lambda: self.save_image(self.lintot_image))
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
        lintot_layout.addWidget(self.lintot_image)
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

        self.spfvside_image = QLabel()
        
        spfvside_buttons = QHBoxLayout()
        self.save_latex_spfvside_button = QPushButton("Save Latex")
        self.save_latex_spfvside_button.clicked.connect(lambda: self.save_latex(self.spfvside_image))
        self.save_latex_spfvside_button.setMaximumWidth(150)
        self.save_image_spfvside_button = QPushButton("Save Image")
        self.save_image_spfvside_button.clicked.connect(lambda: self.save_image(self.spfvside_image))
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
        spfvside_layout.addWidget(self.spfvside_image)
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

        self.graphspfvn_image = QLabel()
       

        graphspfvn_buttons = QHBoxLayout()
        self.save_latex_graphspfvn_button = QPushButton("Save Latex")
        self.save_latex_graphspfvn_button.clicked.connect(lambda: self.save_latex(self.graphspfvn_image))
        self.save_latex_graphspfvn_button.setMaximumWidth(150)
        self.save_image_graphspfvn_button = QPushButton("Save Image")
        self.save_image_graphspfvn_button.clicked.connect(lambda: self.save_image(self.graphspfvn_image))
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
        graphspfvn_layout.addWidget(self.graphspfvn_image)
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
        self.updateData()