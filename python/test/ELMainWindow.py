import sys
import os
import datetime
import configparser
import socket
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QTabWidget, 
    QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, 
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

# add shared directory to python path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "shared")))
from FPIBGclient import TCPIP

# ensure python can find `tabclass.py`
script_dir = os.path.dirname(os.path.abspath(__file__))
shared_path = os.path.abspath(os.path.join(script_dir, "..", "shared"))
if shared_path not in sys.path:
    sys.path.append(shared_path)

from TabClass import *
import inspect

class SetupTab(QWidget):
    # signal for thread-safe ui updates
    received_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # initialize core components
        self.config = configparser.ConfigParser()
        self.client = TCPIP()
        self.connected = False
        self.socket_timeout = 5.0  # 5 second timeout

        # create main layout
        main_layout = QVBoxLayout()

        # network configuration section
        network_layout = QHBoxLayout()
        self.ip_input = QLineEdit(self.client.server_ip)
        self.port_input = QLineEdit(str(self.client.server_port))
        network_layout.addWidget(QLabel("IP:"))
        network_layout.addWidget(self.ip_input)
        network_layout.addWidget(QLabel("Port:"))
        network_layout.addWidget(self.port_input)

        # connection control buttons
        connection_buttons = QHBoxLayout()
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_server)
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.disconnect_button.setEnabled(False)
        connection_buttons.addWidget(self.connect_button)
        connection_buttons.addWidget(self.disconnect_button)

        # command interface section
        communication_layout = QVBoxLayout()
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("enter command...")
        self.command_input.returnPressed.connect(self.send_command)

        # command control buttons
        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_command)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.clear_button)

        # put together communication components
        communication_layout.addWidget(self.output_display)
        communication_layout.addWidget(self.command_input)
        communication_layout.addLayout(button_layout)

        # final layout assembly
        main_layout.addLayout(network_layout)
        main_layout.addLayout(connection_buttons)
        main_layout.addLayout(communication_layout)
        self.setLayout(main_layout)

        # connect signal for thread-safe updates
        self.received_signal.connect(self.display_response)

        # load saved settings
        self.load_config()

    def connect_to_server(self):
        """connect to the server with timeout handling"""
        try:
            # get connection details
            self.client.server_ip = self.ip_input.text().strip()
            self.client.server_port = int(self.port_input.text().strip())
            
            # establish connection
            self.client.openConnection()
            
            # configure socket timeout
            self.client.client_socket.settimeout(self.socket_timeout)
            
            # update ui state
            self.output_display.append(f"connected to {self.client.server_ip}:{self.client.server_port}")
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.ip_input.setEnabled(False)
            self.port_input.setEnabled(False)
            self.connected = True

            # save settings
            self.save_config()

        except Exception as e:
            self.output_display.append(f"connection error: {str(e)}")

    def disconnect_from_server(self):
        """handle server disconnection cleanly"""
        if self.connected:
            self.client.closeConnection()
            self.output_display.append("disconnected from server.")
            
            # reset ui state
            self.ip_input.setEnabled(True)
            self.port_input.setEnabled(True)
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.connected = False

    def send_command(self):
        """send command with threaded response handling"""
        if not self.connected:
            self.output_display.append("not connected to a server.")
            return

        command = self.command_input.text().strip()
        if command:
            try:
                # send the command
                self.client.client_socket.sendall(command.encode('utf-8'))
                self.output_display.append(f"sent: {command}")

                # start response thread
                response_thread = threading.Thread(target=self.receive_response, args=(command,))
                response_thread.daemon = True  # thread will close with main program
                response_thread.start()

                self.command_input.clear()
            except Exception as e:
                self.output_display.append(f"error sending command: {str(e)}")

    def receive_response(self, command):
        """handle server response in separate thread with timeout"""
        try:
            response = self.client.client_socket.recv(1024).decode()
            if not response:
                self.received_signal.emit("server closed connection")
                self.disconnect_from_server()
                return
                
            self.received_signal.emit(response)
            self.log_command(command, response)
            self.save_config()
            
        except socket.timeout:
            self.received_signal.emit("server response timeout")
        except ConnectionError:
            self.received_signal.emit("connection lost")
            self.disconnect_from_server()
        except Exception as e:
            self.received_signal.emit(f"error receiving response: {str(e)}")

    def display_response(self, response):
        """thread-safe method to update ui with response"""
        self.output_display.append(f"received: {response}")

    def log_command(self, command, response):
        """log command and response with timestamp"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("ELLogging.log", "a") as log:
                log.write(f"{timestamp} - command: {command}\n")
                log.write(f"{timestamp} - response: {response}\n")
        except Exception as e:
            self.output_display.append(f"error logging command: {str(e)}")

    def clear_output(self):
        """clear the output display"""
        self.output_display.clear()

    def save_config(self):
        """save all settings to config file"""
        try:
            if 'Settings' not in self.config:
                self.config.add_section('Settings')
            
            # save current settings
            self.config['Settings']['last_command'] = self.command_input.text().strip()
            self.config['Settings']['server_ip'] = self.ip_input.text().strip()
            self.config['Settings']['server_port'] = self.port_input.text().strip()

            with open('ELConfig.cfg', 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            self.output_display.append(f"error saving config: {str(e)}")

    def load_config(self):
        """load saved settings from config file"""
        try:
            self.config.read('ELConfig.cfg')
            if 'Settings' in self.config:
                self.command_input.setText(self.config['Settings'].get('last_command', ''))
                self.ip_input.setText(self.config['Settings'].get('server_ip', '127.0.0.1'))
                self.port_input.setText(self.config['Settings'].get('server_port', '50004'))
        except Exception as e:
            self.output_display.append(f"error loading config: {str(e)}")

class FPIBGMainWin(QWidget):
    def __init__(self, ObjName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ObjName = ObjName
        self.setWindowTitle('fpibg main window')
        self.setGeometry(100, 100, 1024, 768)
        
        # create main layout
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        # create tab widget
        tabs = QTabWidget()
        
        # add general setup tab
        tabSetup = TabObj(self)
        tabSetup.SetForm()
        tabs.addTab(tabSetup, "General")

        # add tcpip setup tab
        self.setup_tab = SetupTab()
        tabs.addTab(self.setup_tab, "Setup")

        # add bottom buttons
        main_layout.addWidget(tabs, 0, 0, 2, 1)
        main_layout.addWidget(QPushButton('save'), 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(QPushButton('cancel'), 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

    def Create(self, FPIBGBase):
        """initialize with base class and log success"""
        self.bs = FPIBGBase
        self.bs.log.log(inspect.currentframe().f_lineno,
                       __file__,
                       inspect.currentframe().f_code.co_name,
                       self.ObjName,
                       0,
                       "test 1 main window success")
        return self

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FPIBGMainWin("FPIBGMainWin")
    window.show()
    sys.exit(app.exec())