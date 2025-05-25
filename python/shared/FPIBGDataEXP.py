import os
import csv
import inspect
import pandas as pd

class DataClass:

    def __init__(self, ObjName):
        super().__init__()
        self.data_files = []
        self.average_list = []
        self.ObjName = ObjName
        
    def Open(self):
        self.Update(self,self.ObjName)

    def Create(self, BaseObj, testType):
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.bobj.lvl = 1000

    def UpdateSummary(self,file_end) -> bool:
        match(file_end):
            case "PQB":
                self.topdirdata = self.cfg.application.testdirPQB
            case "PCD":
                self.topdirdata = self.cfg.application.testdirPCD
            case "DUP":
                self.topdirdata = self.cfg.application.testdirDUP
            case "CFB":
                self.topdirdata = self.cfg.application.testdirCFB
        self.hasData = True
        if os.path.exists(self.topdirdata):
            self.hasData = True
            rettxt = "Sucessfully found data directory :" + self.topdirdata
            self.bobj.log.log(self.bobj.lvl,inspect.currentframe().f_lineno,
            __file__,
            inspect.currentframe().f_code.co_name,
            self.ObjName,
            0,
            rettxt)
        else:
            rettxt = "Data directory :" + self.topdirdata + " not found."
            self.bobj.log.log(self.bobj.lvl, inspect.currentframe().f_lineno,
            __file__,
            inspect.currentframe().f_code.co_name,
            self.ObjName,
            1,
            rettxt)

        if self.check_data_files() == False:
           self.hasData = False     
           return False
        self.create_summary()
        self.get_averages()
        return True

    def Close(self):
        pass

    def Read(self):
        pass

    def Write(self):
        pass

    def new_path(self, dir):
        parts = dir.rsplit("/", 1) 
        parts[-1] = parts[-1].replace("data", "")
        return "/".join(parts)
    
    # Returns column names of the object summary file
    def query(self):
        if(self.hasData == False):
            return ["no data"]
        newdir = self.new_path(self.topdirdata) + ".csv"
        with open(newdir, mode= 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                return row
            
    def return_table(self, colNames):
        if(self.hasData == False):
            return ["no data"]
        newdir = self.new_path(self.topdirdata) + ".csv"
        table = pd.read_csv(newdir, usecols=colNames)
        return table

    # Returns true if number of .tst files equal to number of R or D files
    def check_data_files(self) -> bool:
        if(os.path.exists(self.topdirdata) == False):
            print ("Data Directories not available" )
            return False
        tst_files = [i for i in os.listdir(self.topdirdata) if i.endswith(".tst")]
        self.data_files = [i[:-5] for i in os.listdir(self.topdirdata) if i.endswith("D.csv")]
        self.hasData = len(tst_files) == len(self.data_files)
        if(self.hasData == False):
            return False
        self.data_files = [i[:-5] for i in os.listdir(self.topdirdata) if i.endswith("R.csv")]
        self.hasData = len(tst_files) == len(self.data_files)
        if(self.hasData == False):
            return False
        
        return True
        

    def create_summary(self):
        data = ['Name', 'fps', 'cpums', 'cms', 'gms', 'expectedp', 'loadedp',
                'shaderp_comp', 'shaderp_grph', 'expectedc', 'shaderc', 'sidelen']
        newdir = self.new_path(self.topdirdata) + ".csv"
        with open(newdir, mode= 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def get_averages(self):
        directory = self.new_path(self.topdirdata) + ".csv"
        for i in self.data_files:
            file_path_debug = self.topdirdata + "/" + i + "D.csv"
            file_path_release = self.topdirdata + "/" + i + "R.csv"
            fps = cpums = cms = gms = expectedp = loadedp = shaderp_comp = shaderp_grph = expectedc = shaderc = sidelen = count = 0
            with open(file_path_debug, 'r') as filename:
                file = csv.DictReader(filename)
                for col in file:
                    count += 1
                    expectedp += float(col['expectedp'])
                    loadedp += float(col['loadedp'])
                    shaderp_comp += float(col['shaderp_comp'])
                    shaderp_grph += float(col['shaderp_grph'])
                    expectedc += float(col[' expectedc'])
                    shaderc += float(col['shaderc'])
                    sidelen += float(col[' sidelen'])
            with open(file_path_release, 'r') as filename:
                file = csv.DictReader(filename)
                for col in file:
                    fps += float(col['fps'])
                    cpums += float(col['cpums'])
                    cms += float(col['cms'])
                    gms += float(col['gms'])
            fps = fps / count
            cpums = cpums / count
            cms = cms / count
            gms = gms / count
            expectedp = expectedp / count
            loadedp = loadedp / count
            shaderp_comp = shaderp_comp / count
            shaderp_grph = shaderp_grph / count
            expectedc = expectedc / count
            shaderc = shaderc / count
            sidelen = sidelen / count
            avg_list = [i, fps, cpums, cms, gms, expectedp, loadedp, shaderp_comp,
                        shaderp_grph, expectedc, shaderc, sidelen]
            with open(directory, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(avg_list)
            self.average_list.append(avg_list)