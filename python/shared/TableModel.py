import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

import pandas as pd


class PandasModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            if (index.column() == 0):
                return "%.0f" % value
            
            if (index.column() == 1):
                return "%.2f" % (1000*value)
            
            if (index.column() == 2):
                return "%.2f" % (1000*value)
            
            if (index.column() == 3):
                return "%.2f" % (1000*value)
            
            if (index.column() == 4):
                return "%d" % (value)
            
            if isinstance(value, float):
            # Render float to 2 dp
                return "%.5f" % value

            if isinstance(value, str):
            # Render strings with quotes
                return '"%s"' % value

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])

            #if orientation == Qt.Orientation.Vertical:
              #  return str(self._data.index[section])


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value= self._data[index.row()][index.column()]
            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value
            
            return str(value)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
