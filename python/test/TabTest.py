from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, \
    QTabWidget, QScrollArea, QFormLayout, QLabel


class MyTableWidget(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QScrollArea()

        self.tabs.addTab(self.tab1, 'Tab 1')
        self.tabs.addTab(self.tab2, 'Tab 2')

        content_widget = QWidget()
        self.tab2.setWidget(content_widget)
        flay = QFormLayout(content_widget)
        self.tab2.setWidgetResizable(True)
        self.t1 = QLabel('Test1')
        self.t2 = QLabel('Test2')
        self.t3 = QLabel('Test3')
        self.t4 = QLabel('Test4')
        self.t5 = QLabel('Test5')
        self.t6 = QLabel('Test6')

        flay.addRow(self.t1)
        flay.addRow(self.t2)
        flay.addRow(self.t3)
        flay.addRow(self.t4)
        flay.addRow(self.t5)
        flay.addRow(self.t6)

        self.layout.addWidget(self.tabs)
        self.resize(300, 100)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = MyTableWidget()
    w.show()
    sys.exit(app.exec())