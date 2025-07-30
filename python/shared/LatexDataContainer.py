
from LatexDataCSV import *
from LatexDataParticle import *
class LatexDataContainer():


    def __init__(self, FPIBGBase, ObjName, *args, **kwargs):
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.log.logs(self,"LatexDataContainer finished init.")
        self.data_base = None


    def Create(self, data_type,data_dir,data_file=None):
        self.data_type = data_type.lower()
        matches = ["pqb","pcd","cfb"]
        if "csv" in self.data_type:
            self.data_base = LatexDataCSV(self.bobj,"CSV Data")
            self.data_base.Create(data_type,data_dir,data_file) 
        elif any(x in self.data_type for x in matches):
            self.data_base = LatexDataParticle(self.bobj,"Particle Data")
            self.data_base.Create(data_type,data_dir) 
        else:
            print("Invaid data type at line 26 in Create in LatexDataContainer()")  

    def getData(self):
        return self.data_base.getData()

        
