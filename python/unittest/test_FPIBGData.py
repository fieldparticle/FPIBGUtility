import pytest
import os
import csv
import sys
from typing import Type

# Point ot the shared firectory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared')))
# Get the current working directory and set it to the parent directory.
cwd = os.getcwd()
os.chdir("..\\..\\") 
print(cwd)
# Import requied classes
from FPIBGDataEXP import (DataClass)
from FPIBGBase import *
from mock import mock, Mock
from unittest.mock import mock_open, patch

# Create a fixture to perform class instatiation and base class assignment.
@pytest.fixture(name="dataClass")
def dataClass():
    bc = FPIBGBase("GlobalBaseClass")
    bc.Create("ParticleJB.cfg",'JBLog.log')
    dta = DataClass(True, "ExampleObject")
    dta.Create(bc,"PQB")
    return dta

# Run a test. This test changes the data directory to one that does not exists 
# and tests to insure that it failes
def test_can_find_data_directoryTrue(dataClass):
    # Chnage the data directory to a non-existent location
    dataClass.topdir = "Nonexsitentdirectory"
    # Assert that the function returns false
    assert dataClass.Open() == False
    # Assert that the log line with the correct code was written to the log file
    assert dataClass.log.CheckLogFile("1001") == True


