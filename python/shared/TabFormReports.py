import sys
from FPIBGPlotDataEXP import *
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
from LatexClass import *
from CfgLabel import *
from FPIBGException import *
from LatexSingleImage import *
from LatexMultiImage import *
from LatexPlotBase import *
from LatexSingleTable import *


class TabReports(QTabWidget):

    plotData = PlotData("PlotData")
    cleanPRE = False

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
        self.plotData.Update("PQB")
        self.fpsvn_image.setPixmap(self.plotData.plot_PQBfpsvn(0))
        self.PQBfpsvnltx = LatexSinglePlot(self)
        self.PQBfpsvnltx.Create(self.bobj,"PQBfpsvn")
        self.PQBfpsvnltx.outDirectory = self.cfg.py_plots_dir
        self.PQBfpsvnltx.ltxDirectory = self.cfg.latex_plots_dir
        caption = self.PQBfpsvnltx.readCapFile()
        self.fpsvn_text_edit.setText(caption)

        self.spfvn_image.setPixmap(self.plotData.plot_PQBspfvn(7))
        self.PQBspfvnltx = LatexSinglePlot(self)
        self.PQBspfvnltx.Create(self.bobj,"PQBspfvn")
        self.PQBspfvnltx.outDirectory = self.cfg.py_plots_dir
        self.PQBspfvnltx.ltxDirectory = self.cfg.latex_plots_dir
        caption = self.PQBspfvnltx.readCapFile()
        self.spfvn_text_edit.setText(caption)

        self.lintot_image.setPixmap(self.plotData.plot_PQBlintot(7))
        self.PQBlinTotltx = LatexSinglePlot(self)
        self.PQBlinTotltx.Create(self.bobj,"PQBLinTot")
        self.PQBlinTotltx.outDirectory = self.cfg.py_plots_dir
        self.PQBlinTotltx.ltxDirectory = self.cfg.latex_plots_dir
        caption = self.PQBlinTotltx.readCapFile()
        self.lintot_text_edit.setText(caption)

        ## Uodate Tables
        header = self.plotData.query()
        latexFile = ["fps", "cpums", "cms", "gms", "loadedp"]
        tdata = self.plotData.return_table(latexFile)
        self.PQBTablePerfAll = LatexSingleTable(self)
        self.PQBTablePerfAll.Latex.outDirectory = self.cfg.py_plots_dir
        self.PQBTablePerfAll.Latex.ltxDirectory = self.cfg.latex_tables_dir
        self.table001_image.setModel(self.PQBTablePerfAll)
        self.PQBTablePerfAll.Latex.name = "PQBPerfTable"
        self.table001_text_edit.setText(self.PQBTablePerfAll.Latex.readCapFile())
        self.table001_image.show()

        self.plotData.Update("PCD")
        self.PCDspfvside_image.setPixmap(self.plotData.plot_PCDspfvside())
        self.PCDspfvside = LatexSinglePlot(self)
        self.PCDspfvside.Create(self.bobj,"PCDspfvside")
        self.PCDspfvside.outDirectory = self.cfg.py_plots_dir
        self.PCDspfvside.ltxDirectory = self.cfg.latex_plots_dir
        caption = self.PCDspfvside.readCapFile()
        self.spfvside_text_edit.setText(caption)
    
    def get_output_dir(self):
        return self.folderLineEdit.text()

    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    def save_latex_PQBfpsvn(self):
        self.plotData.Update("PQB")
        if(self.plotData.hasData == True):
            self.plotData.plot_PQBfpsvn(0)
            self.PQBfpsvnltx.cleanPRE = self.cleanPRE                        
            self.PQBfpsvnltx.caption =  self.fpsvn_text_edit.toPlainText()
            self.PQBfpsvnltx.width = 0
            self.PQBfpsvnltx.height = 0
            self.PQBfpsvnltx.title = "TITLE:Plot of fps v loadedp"
            self.PQBfpsvnltx.scale = 0.50
            self.PQBfpsvnltx.fontSize = 10
            self.PQBfpsvnltx.float = False
            self.PQBfpsvnltx.placement = "h"
            self.PQBfpsvnltx.Write(plt)
       
       
    def save_latex_PQBspfvn(self):
        self.plotData.Update("PQB")
        if(self.plotData.hasData == True):
            self.plotData.plot_PQBspfvn(7)
            self.PQBspfvnltx.cleanPRE = self.cleanPRE
            self.PQBspfvnltx.caption =  self.spfvn_text_edit.toPlainText()
            self.PQBspfvnltx.width = 0
            self.PQBspfvnltx.height = 0
            self.PQBspfvnltx.title = "TITLE:spf v loaded p"
            self.PQBspfvnltx.scale = 0.50
            self.PQBspfvnltx.fontSize = 10
            self.PQBspfvnltx.float = False
            self.PQBspfvnltx.placement = "h"
            self.PQBspfvnltx.Write(plt)
            
    def save_latex_PQBLinearityAll(self):
        self.plotData.Update("PQB")
        if(self.plotData.hasData == True):
            self.plotData.plot_PQBlintot(7)
            self.PQBlinTotltx.cleanPRE = self.cleanPRE
            self.PQBlinTotltx.caption =  self.lintot_text_edit.toPlainText()
            self.PQBlinTotltx.width = 0
            self.PQBlinTotltx.height = 0
            self.PQBlinTotltx.title = "TITLE:spf v loaded p"
            self.PQBlinTotltx.scale = 0.50
            self.PQBlinTotltx.fontSize = 10
            self.PQBlinTotltx.float = False
            self.PQBlinTotltx.placement = "h"
            self.PQBlinTotltx.Write(plt)

    def save_latex_PQBTable(self):

        latxheader = ["Total\\\\ \\maxfps{}","CPU \\\\ Time","Compute\\\\(Narrow) \\\\ \\mcpt{}","Graphics\\\\(Broad) \\\\ \\mgpt{}","Particles\\\\in\\\\Dataset"]
        self.PQBTablePerfAll.Latex.cleanPRE = self.cleanPRE
        self.PQBTablePerfAll.Latex.setLatexHeaderArray(latxheader)
        self.PQBTablePerfAll.Latex.saveCaption(self.table001_text_edit.toPlainText() )
        self.PQBTablePerfAll.Latex.WriteLatexTable(2)
        return
    

    def save_PCDspfvside(self):
        self.plotData.Update("PCD")
        if(self.plotData.hasData == True):
            self.plotData.plot_PCDspfvside()
            self.PCDspfvside.cleanPRE = self.cleanPRE
            self.PCDspfvside.caption =  self.spfvside_text_edit.toPlainText()
            self.PCDspfvside.width = 0
            self.PCDspfvside.height = 0
            self.PCDspfvside.title = "TITLE:spf v loaded p"
            self.PCDspfvside.scale = 0.50
            self.PCDspfvside.fontSize = 10
            self.PCDspfvside.float = False
            self.PCDspfvside.placement = "h"
            self.PCDspfvside.Write(plt)


    def save_latex_PQBAll(self):
        self.cleanPRE = True    
        self.save_latex_PQBfpsvn()
        self.save_latex_PQBspfvn()
        self.save_latex_PQBLinearityAll()
        self.cleanPRE = False

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
    

    def Create(self, FPIBGBase):
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        #self.latexDir = self.cfg.latex_dir

        self.plotData.Create(FPIBGBase)
      
        
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
        self.folderLineEdit.setText(self.cfg.tex_out_dir)
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
        self.save_latex_pqb_button = QPushButton("Save Latex PQB All")
        self.save_latex_pqb_button.clicked.connect(self.save_latex_PQBAll)
        self.save_latex_pqb_button.setMaximumWidth(150)
        self.pqb_subreports = QTabWidget()

        ####### FPS v N #######
        self.fpsvn_tab = QWidget()
        fpsvn_layout = QVBoxLayout(self.fpsvn_tab)
        self.fpsvn_image = QLabel()
        fpsvn_buttons = QHBoxLayout()
        spacer = QSpacerItem(40, 2, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.save_latex_fpsvn_button = QPushButton("Save Latex")
        self.save_latex_fpsvn_button.clicked.connect(lambda: self.save_latex_PQBfpsvn())
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
        self.save_latex_spfvn_button.clicked.connect(lambda: self.save_latex_PQBspfvn())
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
        self.save_latex_table001_button.clicked.connect(lambda: self.save_latex_PQBTable())
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
        self.save_latex_lintot_button.clicked.connect(lambda: self.save_latex_PQBLinearityAll())
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

        self.PCDspfvside_image = QLabel()
        
        spfvside_buttons = QHBoxLayout()
        self.save_latex_spfvside_button = QPushButton("Save Latex")
        self.save_latex_spfvside_button.clicked.connect(lambda: self.save_PCDspfvside())
        self.save_latex_spfvside_button.setMaximumWidth(150)
        self.save_image_spfvside_button = QPushButton("Save Image")
        self.save_image_spfvside_button.clicked.connect(lambda: self.save_image())
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
        spfvside_layout.addWidget(self.PCDspfvside_image)
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

        self.graphspfvn_image = QLabel("CFB")
       

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
        #self.cfb_subreports.addTab(self.graphspfvn_tab, "Graphics SPF v N")

        ####### SPf V Sidelength #######
        self.compspfvn_tab = QWidget()
        compspfvn_layout = QVBoxLayout(self.compspfvn_tab)

        self.compspfvn_image = QLabel("CFB")

        compspfvn_buttons = QHBoxLayout()
        self.save_latex_compspfvn_button = QPushButton("Save Latex")
        #self.save_latex_compspfvn_button.clicked.connect(lambda: self.save_latex(self.compspfvn_image))
        self.save_latex_compspfvn_button.setMaximumWidth(150)
        self.save_image_compspfvn_button = QPushButton("Save Image")
        self.save_image_compspfvn_button.clicked.connect(lambda: self.save_image(self.compspfvn_image))
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
        compspfvn_layout.addWidget(self.compspfvn_image)
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