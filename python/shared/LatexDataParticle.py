import pandas as pd
from LatexDataBaseClass import *
import os
import csv
class LatexDataParticle(LatexDataBaseClass):

    sumFile = ""
    average_list = []
    def __init__(self, FPIBGBase, ObjName):
        super().__init__(FPIBGBase, ObjName)
    
    def getData(self):
        return self.data

    def Create(self, data_type,data_dir,data_file= None):
        self.data_type = data_type
        try :
            self.topdir = data_dir + "/perfdata" + data_type
            self.sumFile = self.topdir + "/perfdata" + data_type + ".csv"
        except BaseException as e:
            print(e)
        try :
            self.create_summary()
            self.check_data_files()
            self.get_averages()
        except BaseException as e:
            print(e)
            self.hasData = False
            return None
        self.data = pd.read_csv(self.sumFile,header=0)  

    # Returns true if number of .tst files equal to number of R or D files
    def check_data_files(self) -> bool:
        if(os.path.exists(self.sumFile) == False):
            print ("Data Direcoptries not available" )
            self.hasData = False
            return False
        tst_files = [i for i in os.listdir(self.topdir) if i.endswith(".tst")]
        self.data_files = [i[:-5] for i in os.listdir(self.topdir) if i.endswith("R.csv")]
        self.hasData = len(tst_files) == len(self.data_files)
        if(self.hasData == False):
            print("Raw data file count error")
        return self.hasData
    
    def create_summary(self):
        data = ['Name', 'fps', 'cpums', 'cms', 'gms', 'expectedp', 'loadedp',
                'shaderp_comp', 'shaderp_grph', 'expectedc', 'shaderc', 'sidelen']
        with open(self.sumFile, mode= 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    

    def get_averages(self):
        if(self.hasData == False):
            return
        self.create_summary()
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
            with open(self.sumFile, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(avg_list)
            self.average_list.append(avg_list)
        file.close()