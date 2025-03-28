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

        # Create example report tabs
        self.report_tab1 = QWidget()
        layout1 = QVBoxLayout(self.report_tab1)
        label1 = QLabel("Content of Report Type 1")
        layout1.addWidget(label1)
        self.report_tab1.setLayout(layout1)
        self.report_tabs.addTab(self.report_tab1, "Report Type A")

        self.report_tab2 = QWidget()
        layout2 = QVBoxLayout(self.report_tab2)
        label2 = QLabel("Content of Report Type 2")
        layout2.addWidget(label2)
        self.report_tab2.setLayout(layout2)
        self.report_tabs.addTab(self.report_tab2, "Report Type B")

        # Add the embedded tab widget to the main layout
        main_layout.addWidget(self.report_tabs)

        scroll_area.setWidget(scroll_widget)
        main_window_layout = QVBoxLayout(self)
        main_window_layout.addWidget(scroll_area)
        self.setLayout(main_window_layout)