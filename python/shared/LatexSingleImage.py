from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget,QScrollArea,QVBoxLayout,QTabWidget,QFileDialog
from PyQt6.QtGui import QPixmap
from CfgLabel import *
from LatexClass import *
from LatexConfigurationClass import *
class LatexSingleImage(LatexConfigurationClass):
    objArry = []
    dictTab = []
    tabCount = 0
    layouts = []
    lyCount = 0
    LatexFileImage = LatexImageWriter("LatexClass")


    def __init__(self,Parent):
        self.Parent = Parent
        self.bobj = self.Parent.bobj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.itemcfg = Parent.itemcfg 

    def setTypeText(self,Text):
        self.type_text.setTypeText(Text)
        
    
    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    def updateCfgData(self):
        for oob in self.objArry:
            oob.updateCFGData()
        self.itemcfg.updateCfg()
        self.LatexFileImage.Write(self.itemcfg.config) 

    
    def filesChanged(self,path):
        #self.images_name_text.setText(os.path.splitext(os.path.basename(path))[0])
        self.images_name_text.setText(os.path.basename(path))
        self.name_text.setText(os.path.splitext(os.path.basename(path))[0])
    
    

    def OpenLatxCFG(self):
        print(self.itemcfg)
        self.LatexFileImage.outDirectory = self.itemcfg.config.tex_dir
        self.LatexFileImage.ltxDirectory = self.itemcfg.config.tex_image_dir
        self.doItems(self.itemcfg.config)
    
    def clearLayout(self,layout):
        print("-- -- input layout: "+str(layout))
        for i in reversed(range(layout.count())):
            layoutItem = layout.itemAt(i)
            if layoutItem.widget() is not None:
                widgetToRemove = layoutItem.widget()
                print("found widget: " + str(widgetToRemove))
                widgetToRemove.setParent(None)
                layout.removeWidget(widgetToRemove)
            elif layoutItem.spacerItem() is not None:
                print("found spacer: " + str(layoutItem.spacerItem()))
            else:
                layoutToRemove = layout.itemAt(i)
                print("-- found Layout: "+str(layoutToRemove))
                self.clearLayout(layoutToRemove)

    def clearConfigGrp(self):
        del self.objArry [:]
        del self.dictTab[:]
        self.tabCount = 0
        del self.layouts[:]
        self.lyCount = 0
        self.clearLayout(self.cfglayout)

    def setConfigGroup(self,layout):
        self.ConfigGroup = QGroupBox("Latex File Configuration")
        layout.addWidget(self.ConfigGroup,1,0,1,1,alignment= Qt.AlignmentFlag.AlignLeft)
        self.cfglayout = QVBoxLayout()
        self.setSize(self.ConfigGroup,400,500) 
        self.ConfigGroup.setLayout(self.cfglayout)
        self.tabs = QTabWidget()
        self.cfglayout.addWidget(self.tabs)
        self.scrollArea = QScrollArea()
        self.dictTab.append(self.scrollArea)
        content_widget = QWidget()
        content_widget.setStyleSheet('background-color: 111111;')
        self.dictTab[self.tabCount].setWidget(content_widget)
        self.layouts.append(QVBoxLayout(content_widget))
        self.dictTab[self.tabCount].setWidgetResizable(True)
        

    def setImgGroup(self,layout):
        ## Image Interface
        self.imgmgrp = QGroupBox("Image Interface")
        self.setSize(self.imgmgrp,20,20)
        #tab_layout.addWidget(self.imgmgrp,0,3,2,2)
        layout.addWidget(self.imgmgrp,0,3,2,2)
        imagelo = QGridLayout()
        self.imgmgrp.setLayout(imagelo)

        self.image = QLabel()
        self.image.setStyleSheet("background-color:  #ffffff")
        self.setSize(self.image,15,15)
        imagelo.addWidget(self.image,1,0,alignment= Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.ImageName = self.itemcfg.config.images_name_text
        self.ImagePath = self.itemcfg.config.tex_dir + "/" + self.ImageName
        self.pixmap = QPixmap(self.ImagePath)
        self.setSize(self.imgmgrp,self.pixmap.height()+20,self.pixmap.width()) 
        self.setSize(self.image,self.pixmap.height()+20,self.pixmap.width()) 
        self.image.setPixmap(self.pixmap)
        self.LatexFileImage.outDirectory = self.itemcfg.config.tex_dir
        self.LatexFileImage.ltxDirectory = self.itemcfg.config.tex_image_dir
        return self.imgmgrp
    
        

   
    
 

   