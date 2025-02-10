import pytest
import os
import csv
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared')))

from dataclass import (DataClass)

def test_check_data_files():
    testdata = DataClass(True, "PQB")
    assert testdata.check_data_files() == True

def test_create_summary():
    testdata = DataClass(True, "PQB")
    csv_name = "../../../..FPIBGData/perfPQB.csv"
    testdata.create_summary()
    if os.path.exists(csv_name):
        assert True
    else:
        assert False
    
def test_get_averages():
    testdata = DataClass(True, "PQB")
    csv_name = "../../../../FPIBGData/perfPQB.csv"
    testdata.check_data_files()
    testdata.create_summary()
    testdata.get_averages()
    with open(csv_name, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

