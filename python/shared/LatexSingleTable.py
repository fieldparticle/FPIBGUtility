from PyQt6.QtCore import Qt,QAbstractTableModel
from PyQt6.QtWidgets import QTableView
from CfgLabel import *
from LatexClass import *
from LatexConfigurationClass import *
import pandas as pd
import numpy as np

class LatexSingleTable(LatexConfigurationClass):

    tableModel = None
    def __init__(self,Parent,itemCFG=None):
        self.Parent = Parent
        self.bobj = self.Parent.bobj
        self.log = self.bobj.log
        self.cfg = Parent.itemcfg.config 
        self.itemcfg = Parent.itemcfg 
        self.LatexTable = LatexTableWriter(self.Parent)

    def updateCfgData(self):
        for oob in self.objArry:
            oob.updateCFGData()
        self.itemcfg.updateCfg()
        self.LatexTable.Write() 

    def itemChanged(self,key,value):
        pass

    def OpenLatxCFG(self):
        print(self.itemcfg)
        self.doItems(self.itemcfg.config)
        self.updateTableData()

    def updateTableData(self):
        temp_ary = []
        self.data = pd.read_csv(self.cfg.data_file,header=0)  
        temp_ary = []
        # allocate a attribute dictionary
        fld = AttrDictFields()
        for name, df in self.data.items():
            fld[name] = self.data[name]
        for k,v in self.cfg.command_dict.items():
            plotGrouptxt = "DataFields" + str(1)
            if plotGrouptxt in k:
                for ii in range(len(v)):
                    if any(map(lambda char: char in v[ii], "+-/*")):
                        field = eval(v[ii])
                        temp_ary.append(field)
                    else:
                        # Else strip the fld. from the field and get the array at that column name
                        fldtxt = v[ii].split('.')
                        temp_ary.append(self.data[fldtxt[1]])
                    self.onpdata = np.array(temp_ary)   
                temp_ary = []
                  
        self.LatexTable.Create(self.onpdata)
        self.hasPlot = True

   
    
    def setImgGroup(self,layout):
        ## Image Interface
        self.imageGroupLayout = QGridLayout()
        self.Parent.imgmgrp.setLayout(self.imageGroupLayout)
        self.image = QTableView()
        self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,15,15)
        self.imageGroupLayout.addWidget(self.image,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setSize(self.Parent.imgmgrp,700,650) 
        self.setSize(self.image,700,650) 
        return self.Parent.imgmgrp

class SingleTableWidget(QAbstractTableModel):
    
    def __init__(self, data):
        super().__init__()
        self._data = data
        
    rowlength = 0
    collength = 0
    def data(self, index, role):
        #self.Latex.setLatexData(self)
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
            

    
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