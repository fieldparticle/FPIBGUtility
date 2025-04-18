import os
import csv
import inspect

class DataClass:

    def __init__(self, ObjName):
        self.data_files = []
        self.average_list = []
        self.ObjName = ObjName
        


    def Create(self, BaseObj):
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.bobj.lvl = 1000
        
        
      
                

    def Open(self,file_end):
        match(file_end):
            case "PQB":
                self.topdir = self.cfg.application.testdirPQB
            case "PCD":
                self.topdir = self.cfg.application.testdirPCD
            case "DUP":
                self.topdir = self.cfg.application.testdirDUP
            case "CFB":
                self.topdir = self.cfg.application.testdirCFB
        
        if os.path.exists(self.topdir):
            rettxt = "Sucessfully found data directory :" + self.topdir
            self.bobj.log.log(self.bobj.lvl,inspect.currentframe().f_lineno,
            __file__,
            inspect.currentframe().f_code.co_name,
            self.ObjName,
            0,
            rettxt)
        else:
            rettxt = "Data directory :" + self.topdir + " not found."
            self.bobj.log.log(self.bobj.lvl, inspect.currentframe().f_lineno,
            __file__,
            inspect.currentframe().f_code.co_name,
            self.ObjName,
            1,
            rettxt)

    def Close(self):
        pass

    def Read(self):
        pass

    def Write(self):
        pass

    # Returns true if number of .tst files equal to number of R or D files
    def check_data_files(self) -> bool:
        tst_files = [i for i in os.listdir(self.topdir) if i.endswith(".tst")]
        self.data_files = [i[:-5] for i in os.listdir(self.topdir) if i.endswith("D.csv")]
        return len(tst_files) == len(self.data_files)

    def new_path(self, dir):
        parts = dir.rsplit("/", 1) 
        parts[-1] = parts[-1].replace("data", "")
        return "/".join(parts)

    def create_summary(self):
        data = ['Name', 'fps', 'cpums', 'cms', 'gms', 'expectedp', 'loadedp',
                'shaderp_comp', 'shaderp_grph', 'expectedc', 'shaderc', 'sidelen']
        newdir = self.new_path(self.topdir) + ".csv"
        with open(newdir, mode= 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def get_averages(self):
        directory = self.new_path(self.topdir) + ".csv"
        for i in self.data_files:
            file_path_debug = self.topdir + "/" + i + "D.csv"
            file_path_release = self.topdir + "/" + i + "R.csv"
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