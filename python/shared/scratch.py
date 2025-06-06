import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QLabel, QVBoxLayout, QWidget, QHBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multiple Buttons Example")
        self.setGeometry(100, 100, 500, 200)

        # Create central widget and layouts
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # Create a label to display results
        self.result_label = QLabel("Select a city by clicking a button:")
        main_layout.addWidget(self.result_label)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create multiple buttons for different cities
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Miami"]
        self.buttons = []

        for city in cities:
            button = QPushButton(city)
            # Connect each button to the same slot
            button.clicked.connect(self.city_button_clicked)
            button_layout.addWidget(button)
            self.buttons.append(button)

        main_layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)

    # Define the slot to handle all button clicks
    def city_button_clicked(self):
        # sender() returns the button that was clicked
        button = self.sender()
        if button:
            self.result_label.setText(f"You selected: {button.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())