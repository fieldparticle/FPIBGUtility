import os
import sys

from PyQt6 import QtCore, QtWidgets, QtNetwork

import QTermWidget


class RemoteTerm(QTermWidget.QTermWidget):
    def __init__(self, ipaddr, port, parent=None):
        super().__init__(0, parent)

        self.socket = QtNetwork.QTcpSocket(self)

        self.socket.error.connect(self.atError)
        self.socket.readyRead.connect(self.on_readyRead)
        self.sendData.connect(self.socket.write)

        self.startTerminalTeletype()
        self.socket.connectToHost(ipaddr, port)

    @QtCore.pyqtSlot()
    def on_readyRead(self):
        data = self.socket.readAll().data()
        os.write(self.getPtySlaveFd(), data)

    @QtCore.pyqtSlot()
    def atError(self):
        print(self.socket.errorString())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    QtCore.QCoreApplication.setApplicationName("QTermWidget Test")
    QtCore.QCoreApplication.setApplicationVersion("1.0")

    parser = QtCore.QCommandLineParser()
    parser.addHelpOption()
    parser.addVersionOption()
    parser.setApplicationDescription(
        "Example(client-side) for remote terminal of QTermWidget"
    )
    parser.addPositionalArgument("ipaddr", "adrress of host")
    parser.addPositionalArgument("port", "port of host")

    parser.process(QtCore.QCoreApplication.arguments())

    requiredArguments = parser.positionalArguments()
    if len(requiredArguments) != 2:
        parser.showHelp(1)
        sys.exit(-1)

    address, port = requiredArguments
    w = RemoteTerm(QtNetwork.QHostAddress(address), int(port))
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())