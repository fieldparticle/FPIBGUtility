import os
import csv


class DataClass:

    def __init__(self, drflag, ObjName):
        self.m_drflag = drflag
        self.data_files = []
        self.average_list = []
        self.ObjName = ObjName

    def Create(self, BaseObj, file_end):
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        
        match(file_end):
            case "PQB":
                self.topdir = self.cfg.application.testdirPQB
            case "PCD":
                self.topdir = self.cfg.application.testdirPCD
            case "DUP":
                self.topdir = self.cfg.application.testdirDUP
            case "CFB":
                self.topdir = self.cfg.application.testdirCFB
                

    def Open(self):
        pass

    def Close(self):
        pass

    def Read(self):
        pass

    def Write(self):
        pass

    # Returns true if number of .tst files equal to number of R or D files
    def check_data_files(self) -> bool:
        tst_files = [i for i in os.listdir(self.topdir) if i.endswith(".tst")]
        dr_ext = "D.csv" if self.m_drflag else "R.csv"
        self.data_files = [i for i in os.listdir(self.topdir) if i.endswith(dr_ext)]
        return len(tst_files) == len(self.data_files)

    def new_path(self, dir):
        parts = dir.rsplit("/", 1) 
        parts[-1] = parts[-1].replace("data", "")
        return "/".join(parts)

    def create_summary(self):
        data = ['Name', 'fps', 'cpums', 'cms', 'gms']
        newdir = self.new_path(self.topdir) + ".csv"
        with open(newdir, mode= 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def get_averages(self):
        directory = self.new_path(self.topdir) + ".csv"
        for i in self.data_files:
            file_path = self.topdir + "/" + i
            fps = cpums = cms = gms = count = 0
            with open(file_path, 'r') as filename:
                file = csv.DictReader(filename)
                for col in file:
                    count += 1
                    fps += float(col['fps'])
                    cpums += float(col['cpums'])
                    cms += float(col['cms'])
                    gms += float(col['gms'])
            fps = fps / count
            cpums = cpums / count
            cms = cms / count
            gms = gms / count
            avg_list = [i, fps, cpums, cms, gms]
            with open(directory, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(avg_list)
            self.average_list.append(avg_list)