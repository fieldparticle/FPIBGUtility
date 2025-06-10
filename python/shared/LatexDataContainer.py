

from LatexDataParticle import *
class LatexDataContainer():


    def __init__(self, FPIBGBase, ObjName, *args, **kwargs):
        self.ObjName = ObjName
        self.bobj = FPIBGBase
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.log.logs(self,"LatexDataContainer finished init.")
        self.data_base = None


    def Create(self, data_type,data_dir):
        self.data_type = data_type.lower()
        matches = ["pqb","pcd","cfb"]
        if "csv" in self.data_type:
            #self.data_base = DataCSV()
            pass
        if any(x in self.data_type for x in matches):
            self.data_base = LatexDataParticle(self.bobj,"Particle Data")
            self.data_base.Create(data_type,data_dir) 
        else:
            print("Invalisd data type LatexDataParticle")  

    def getData(self):
        return self.data_base.getData()

        
