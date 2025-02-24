import sys
import os
import datetime
import configparser
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QTabWidget, 
    QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, 
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt

# ensure python can find `tabclass.py`
script_dir = os.path.dirname(os.path.abspath(__file__))
shared_path = os.path.abspath(os.path.join(script_dir, "..", "shared"))

if shared_path not in sys.path:
    sys.path.append(shared_path)

from TabClass import *
import inspect

class SetupTab(QWidget):
    def __init__(self):
        super().__init__()

        self.config = configparser.ConfigParser()

        main_layout = QVBoxLayout()

        top_row = QHBoxLayout()

        top_left_frame = QFrame()
        top_left_frame.setFrameShape(QFrame.Shape.Box)
        top_left_frame.setFrameShadow(QFrame.Shadow.Raised)
        top_left_layout = QVBoxLayout()
        top_left_label = QLabel("Top Left Box")
        top_left_layout.addWidget(top_left_label)
        top_left_frame.setLayout(top_left_layout)

        top_right_frame = QFrame()
        top_right_frame.setFrameShape(QFrame.Shape.Box)
        top_right_frame.setFrameShadow(QFrame.Shadow.Raised)
        top_right_layout = QVBoxLayout()
        top_right_label = QLabel("Top Right Box")
        top_right_layout.addWidget(top_right_label)
        top_right_frame.setLayout(top_right_layout)

        top_row.addWidget(top_left_frame, 1)
        top_row.addWidget(top_right_frame, 1)

        communication_layout = QVBoxLayout()
        communication_label = QLabel("Communication Window")

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")
        self.command_input.returnPressed.connect(self.send_command)

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_command)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.clear_button)

        communication_layout.addWidget(communication_label)
        communication_layout.addWidget(self.command_input)
        communication_layout.addLayout(button_layout)
        communication_layout.addWidget(self.output_display)

        main_layout.addLayout(top_row, 1)
        main_layout.addLayout(communication_layout, 2)

        self.setLayout(main_layout)

        self.load_config()

    def clear_output(self):
        self.output_display.clear()

    def send_command(self):
        try:
            command = self.command_input.text().strip()
            if command:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                response = f"[{timestamp}]\nSent: {command}\nResponse: OK"
                self.output_display.append(response)
                self.log_command(command)
                self.save_config(command)
                self.command_input.clear()
        except Exception as e:
            self.output_display.append(f"Error processing command: {str(e)}")

    def log_command(self, command):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("ELLogging.log", "a") as log:
                log.write(f"{timestamp} - Command: {command}\n")
        except Exception as e:
            self.output_display.append(f"Error logging command: {str(e)}")

    def save_config(self, command):
        try:
            if 'LastCommand' not in self.config:
                self.config.add_section('LastCommand')
            self.config['LastCommand']['command'] = command
            with open('ELConfig.cfg', 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            self.output_display.append(f"Error saving config: {str(e)}")

    def load_config(self):
        try:
            self.config.read('ELConfig.cfg')
            if 'LastCommand' in self.config:
                last_command = self.config['LastCommand'].get('command', '')
                if hasattr(self, 'command_input'):
                    self.command_input.setText(last_command)
        except Exception as e:
            if hasattr(self, 'output_display'):
                self.output_display.append(f"Error loading config: {str(e)}")

class FPIBGMainWin(QWidget):
    def __init__(self, ObjName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ObjName = ObjName
        self.setWindowTitle('FPIBG Main Window')
        self.setGeometry(100, 100, 1024, 768)
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        tabs = QTabWidget()
        tabSetup = TabObj(self)
        tabSetup.SetForm()
        tabs.addTab(tabSetup, "General Setup")

        self.setup_tab = SetupTab()
        tabs.addTab(self.setup_tab, "Setup Tab")

        main_layout.addWidget(tabs, 0, 0, 2, 1)
        main_layout.addWidget(QPushButton('Save'), 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(QPushButton('Cancel'), 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

    def Create(self, FPIBGBase):
        self.bs = FPIBGBase
        self.bs.log.log(inspect.currentframe().f_lineno,
                       __file__,
                       inspect.currentframe().f_code.co_name,
                       self.ObjName,
                       0,
                       "Test 1 Main Window Success")
        return self

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FPIBGMainWin("FPIBGMainWin")
    window.show()
    sys.exit(app.exec())
