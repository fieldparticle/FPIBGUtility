
class BrowseButton:

  def __init__(self, FPIBGBase, ObjName,Parent):
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.Parent = Parent
        self.itemcfg = Parent.itemcfg 


    
