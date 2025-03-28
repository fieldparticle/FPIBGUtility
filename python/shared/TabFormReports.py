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


        group_box = QGroupBox("Report Options")
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Parameter 1:"), QLineEdit())
        form_layout.addRow(QLabel("Parameter 2:"), QLineEdit())
        generate_button = QPushButton("Generate Report")
        form_layout.addRow(generate_button)
        group_box.setLayout(form_layout)
        main_layout.addWidget(group_box)

        # --- Embedded QTabWidget for reports ---
        self.report_tabs = QTabWidget()

        #########################
        #### PQB REPORT TABS ####
        #########################
        self.pqb_tab = QWidget()
        pqb_layout = QVBoxLayout(self.pqb_tab)
        # label1 = QLabel("Content of Report Type 1")
        self.pqb_subreports = QTabWidget()

        self.fpsvn_tab = QWidget()
        fpsvn_layout = QVBoxLayout(self.fpsvn_tab)
        #TODO: Insert fpsvn content here
        #END fpsvn content
        self.fpsvn_tab.setLayout(fpsvn_layout)
        self.pqb_subreports.addTab(self.fpsvn_tab, "FPS v N")

        self.spfvn_tab = QWidget()
        spfvn_layout = QVBoxLayout(self.spfvn_tab)
        #TODO: Insert spfvn content here
        #END spfvn content
        self.spfvn_tab.setLayout(spfvn_layout)
        self.pqb_subreports.addTab(self.spfvn_tab, "SPF v N")

        self.table001_tab = QWidget()
        table001_layout = QVBoxLayout(self.table001_tab)
        #TODO: Insert Table001 content here
        #END Table001 content
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

        pqb_layout.addWidget(self.pqb_subreports)
        # pqb_layout.addWidget(label1)
        self.pqb_tab.setLayout(pqb_layout)
        self.report_tabs.addTab(self.pqb_tab, "PQB")

        #########################
        #### PCD REPORT TABS ####
        #########################
        self.pcd_tab = QWidget()
        pcd_layout = QVBoxLayout(self.pcd_tab)
        # label2 = QLabel("Content of Report Type 2")
        self.pcd_subreports = QTabWidget()

        self.spfvside_tab = QWidget()
        spfvside_layout = QVBoxLayout(self.spfvside_tab)
        #TODO: Insert fpsvn content here
        #END fpsvn content
        self.spfvside_tab.setLayout(spfvside_layout)
        self.pcd_subreports.addTab(self.spfvside_tab, "SPf V Sidelength")

        pcd_layout.addWidget(self.pcd_subreports)
        # pcd_layout.addWidget(label2)
        self.pcd_tab.setLayout(pcd_layout)
        self.report_tabs.addTab(self.pcd_tab, "PCD")

        #########################
        #### CFB REPORT TABS ####
        #########################
        self.cfb_tab = QWidget()
        cfb_layout = QVBoxLayout(self.cfb_tab)
        # label2 = QLabel("Content of Report Type 2")
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