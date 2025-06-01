from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget,QScrollArea,QVBoxLayout,QTabWidget,QFileDialog
from PyQt6.QtGui import QPixmap
from CfgLabel import *
from LatexClass import *
from LatexConfigurationClass import *

class LatexMultiImage(LatexConfigurationClass):

    def __init__(self,Parent):
        self.Parent = Parent
        self.bobj = self.Parent.bobj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.itemcfg = Parent.itemcfg
        self.tab_layout =  Parent.tab_layout

   