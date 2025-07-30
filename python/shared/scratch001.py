import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMainWindow,QGridLayout
from PyQt6.QtCore import pyqtSignal, pyqtSlot

class CustomDialog(QDialog):
    data_submitted = pyqtSignal(str,str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Passing Dialog')
        self.setGeometry(100, 100, 300, 150)

        layout = QGridLayout()

        self.key_label = QLabel('Enter some data:')
        layout.addWidget(self.key_label,0,0)

        self.key_edit = QLineEdit()
        layout.addWidget(self.key_edit,0,1)

        self.value_label = QLabel('Enter some data:')
        layout.addWidget(self.value_label,1,0)

        self.value_edit = QLineEdit()
        layout.addWidget(self.value_edit,1,1)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_data(self):
        key_data = self.key_edit.text()
        val_data = self.value_edit.text()
        self.data_submitted.emit(key_data,val_data)
        self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 400, 200)

        self.button = QPushButton('Open Dialog', self)
        self.button.setGeometry(100, 100, 200, 50)
        self.button.clicked.connect(self.open_dialog)

        self.label = QLabel('Data from dialog will appear here', self)
        self.label.setGeometry(100, 50, 200, 50)

    def open_dialog(self):
        dialog = CustomDialog()
        dialog.data_submitted.connect(self.handle_data)
        dialog.exec()

    @pyqtSlot(str,str)
    def handle_data(self, key_data,val_data):
        self.label.setText(f'Key: {key_data} Val: {val_data}')
       
# Create an instance of QApplication
app = QApplication(sys.argv)

# Create and display the main window
main_window = MainWindow()
main_window.show()

# Run the application's event loop
sys.exit(app.exec())