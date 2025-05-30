from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget,QScrollArea,QVBoxLayout,QTabWidget,QFileDialog
from PyQt6.QtGui import QPixmap
from CfgLabel import *
from LatexClass import *

class LatexSingleImage():
    objArry = []
    dictTab = []
    tabCount = 0
    layouts = []
    lyCount = 0
    LatexFileImage = LatexImage("LatexClass")


    def __init__(self, FPIBGBase, ObjName,Parent):
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.Parent = Parent
        self.itemcfg = Parent.itemcfg 

    def setTypeText(self,Text):
        self.type_text.setTypeText(Text)
        
    
    def setSize(self,control,H,W):
        control.setMinimumHeight(H)
        control.setMinimumWidth(W)
        control.setMaximumHeight(H)
        control.setMaximumWidth(W)

    
    def filesChanged(self,path):
        #self.images_name_text.setText(os.path.splitext(os.path.basename(path))[0])
        self.images_name_text.setText(os.path.basename(path))
        self.name_text.setText(os.path.splitext(os.path.basename(path))[0])
    
    def save_latex_Image(self):
        self.itemcfg.updateCfg()
        self.LatexFileImage.Create(self.bobj,self.itemcfg.config.name_text)
        self.LatexFileImage.cleanPRE = True
        self.LatexFileImage.width = 0
        self.LatexFileImage.height = 0

        for oob in self.objArry:
            if "type_text" in oob.key:
                self.LatexFileImage.type = oob.value
            if "caption_box" in oob.key:
                self.LatexFileImage.caption = oob.value
            if "title_text" in oob.key:
                self.LatexFileImage.title = oob.value
            if "scale_text" in oob.key:
                self.LatexFileImage.scale = oob.value
            if "font_size" in oob.key:
                self.LatexFileImage.fontSize = oob.value
            if "floating_bool" in oob.key:
                self.LatexFileImage.float = oob.value
            if "placement_text" in oob.key:                
                self.LatexFileImage.placement = oob.value
            if "scale_text" in oob.key:                
                self.LatexFileImage.scale = oob.value
        self.LatexFileImage.Write(self.itemcfg.config) 
    
    def OpenLatxCFG(self):
        print(self.itemcfg)
        self.ImageName = self.itemcfg.config.images_name_text
        self.ImagePath = self.itemcfg.config.tex_dir + "/" + self.ImageName
        self.pixmap = QPixmap(self.ImagePath)
        self.setSize(self.imgmgrp,self.pixmap.height()+20,self.pixmap.width()) 
        self.setSize(self.image,self.pixmap.height()+20,self.pixmap.width()) 
        self.image.setPixmap(self.pixmap)
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
        self.setSize(self.ConfigGroup,400,400) 
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
        
        #tab_layout.addWidget(self.ConfigGroup)

    def setImgGroup(self,layout):
            # -------------------------------------------------------------
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
            return self.imgmgrp

    def doItems(self,cfg):
        self.tabCount+=1
        self.lyCount +=1
        self.dictTab.append(QScrollArea())
        self.tabs.addTab(self.dictTab[self.tabCount],"Config Items")
        content_widget = QWidget()
        content_widget.setStyleSheet('background-color: 111111;')
        self.dictTab[self.tabCount].setWidget(content_widget)
        self.layouts.append(QVBoxLayout(content_widget))
        self.dictTab[self.tabCount].setWidgetResizable(True)
        self.cfgHeight = 0
        for k ,v in cfg.items():
            if type(v) == list :
                print("List",k,len(v))
            elif type(v) == str:
                H,W = self.doString(cfg,k,v)
                self.cfgHeight += H
            elif type(v) == bool:
                print("Str",k,v)
                widget = CfgBool(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg))
                self.objArry.append(widget)
                self.cfgHeight += 70
            elif type(v) == int:
                print("int",k,v)
                widget = CfgInt(k,v)
                self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg))
                self.objArry.append(widget)    
                self.cfgHeight += 70
            elif type(v) == tuple   :
               H,W = self.doArray(cfg,k,v)
               self.cfgHeight += H
        #self.setSize(self.ConfigGroup,self.cfgHeight,450)
             
    def doArray(self,cfg,k,v):
        print("tuple",k,len(v))
        widget = CfgArray(k,v)
        self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg,self))    
        #H,W = widget.setHW(30,250)
        H,W = widget.getHW()
        return H,W
    
    def doString(self,cfg,k,v):
        print("Str",k,len(v))
        H = 0
        W = 0
        if "caption" in k:
            widget = CfgTextBox(k,v)
            self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg))
            H,W = widget.setHW(100,250)
            self.objArry.append(widget)
        elif "type_text" in k:
            self.type_text = CfgString(k,v,self)
            self.layouts[self.lyCount].addWidget(self.type_text.Create(cfg,self.itemcfg))
            H,W = self.type_text.setHW(30,250)     
            self.objArry.append(self.type_text)
        elif "images_name_text" in k:
            self.images_name_text = CfgString(k,v,self)
            self.layouts[self.lyCount].addWidget(self.images_name_text.Create(cfg,self.itemcfg))
            H,W = self.images_name_text.setHW(30,250)     
            self.objArry.append(self.images_name_text)
        elif "name_text" in k:
            self.name_text = CfgString(k,v,self)
            self.layouts[self.lyCount].addWidget(self.name_text.Create(cfg,self.itemcfg))
            H,W = self.name_text.setHW(30,250)     
            self.objArry.append(self.name_text)
        elif "tex_dir" in k:
            self.tex_dir = CfgString(k,v,self)
            self.tex_dir.setAsDir()
            self.layouts[self.lyCount].addWidget(self.tex_dir.Create(cfg,self.itemcfg))
            H,W = self.tex_dir.setHW(100,250)
            self.objArry.append(self.tex_dir)  
        elif "dir" in k:
            widget = CfgString(k,v,self)
            widget.setAsDir()
            self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg))
            H,W = widget.setHW(100,250)
            self.objArry.append(widget)
        elif "file" in k:
            widget = CfgString(k,v,self)
            widget.setAsFile()
            self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg))
            H,W = widget.setHW(100,250)
            self.objArry.append(widget)
        else:
            widget = CfgString(k,v,self)
            self.layouts[self.lyCount].addWidget(widget.Create(cfg,self.itemcfg))
            H,W = widget.setHW(30,250)
            self.objArry.append(widget)
        
        return H,W
    
    
 

   