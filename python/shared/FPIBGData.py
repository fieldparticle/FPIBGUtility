import os
import csv


class DataClass:

    def __init__(self, drflag, data_name):
        self.m_drflag = drflag
        self.data_files = []
        self.data_name = data_name

    # Returns true if number of .tst files equal to number of R or D files
    def check_data_files(self) -> bool:
        directory = "C:/FPIBGData/FPIBGData/perfdata" + self.data_name
        tst_files = [i for i in os.listdir(directory) if i.endswith(".tst")]
        dr_ext = "D.csv" if self.m_drflag else "R.csv"
        self.data_files = [i for i in os.listdir(directory) if i.endswith(dr_ext)]
        return len(tst_files) == len(self.data_files)

    def create_summary(self):
        csv_name = "C:/FPIBGData/FPIBGData/perf" + self.data_name + ".csv"
        data = ['Name', 'fps', 'cpums', 'cms', 'gms']
        with open(csv_name, mode= 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def get_averages(self):
        directory = "C:/FPIBGData/FPIBGData/perf" + self.data_name + ".csv"
        for i in self.data_files:
            file_path = "C:/FPIBGData/FPIBGData/perfData" + self.data_name + "/" + i
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
            average_list = [i, fps, cpums, cms, gms]
            with open(directory, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(average_list)