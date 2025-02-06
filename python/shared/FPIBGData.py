import os
import csv


class DataClass:

    def __init__(self, drflag, data_name):
        self.m_drflag = drflag
        self.data_files = []
        self.data_name = data_name

    # Returns true if number of .tst files equal to number of R or D files
    def check_data_files(self) -> bool:
        directory = "../../../../FPIBGData/perfdata" + self.data_name
        tst_files = [i for i in os.listdir(directory) if i.endswith(".tst")]
        dr_ext = "D.csv" if self.m_drflag else "R.csv"
        self.data_files = [i for i in os.listdir(directory) if i.endswith(dr_ext)]
        return len(tst_files) == len(self.data_files)

    def create_summary(self):
        csv_name = "../../../../FPIBGData/perf" + self.data_name + ".csv"
        data = ['Name', 'fps', 'cpnums', 'cms', 'gms']
        with open(csv_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def get_averages(self):
        for i in self.data_files:
            fps, cpnums, cms, gms, count = 0
            filename = open(i, 'r')
            file = csv.DictReader(filename)
            for col in file:
                count += 1
                fps += col['fps']
                cpnums += col['cpnums']
                cms += col['cms']
                gms += col['gms']
            fps = fps / count
            cpnums = cpnums / count
            cms = cms / count
            gms = gms / count
            average_list = [i, fps, cpnums, cms, gms]
            self.writeToFile(average_list)

    def writeToFile(self, averages: list):
        directory = "../../../../FPIBGData/perf" + self.data_name + ".csv"
        with open(directory, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(averages)