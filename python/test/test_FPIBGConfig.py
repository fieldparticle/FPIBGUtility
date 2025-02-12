import os
import sys

def get_repo_root():
    """Gets the absolute path of the git repo root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while not os.path.exists(os.path.join(current_dir, ".git")):
        current_dir = os.path.dirname(current_dir)
        if current_dir == "/":
            raise FileNotFoundError("Could not find .git directory")
    return current_dir

sharedDir = get_repo_root() + "/python/shared"

sys.path.append(os.path.abspath(sharedDir))

from FPIBGConfig import *
from FPIBGLog import *

# def test_name():
#     cObj = FPIBGConfig()
#     cDict = cObj.GetConfig()
#     assert cDict.name == "particleOnly"

def main():
    cObj = FPIBGConfig("ConfigObject")
    log = FPIBGLog("GlobalLoggingObject")   
    log.Create()
    log.Open()
    cObj.Create(log)
    cObj.testObject(1,5)
    


if __name__ == "__main__":
    main()