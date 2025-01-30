from FPIBGLog import FPIBGLog
from FPIBGConfig import FPIBGConfig


## FPBIG Base class. This class is passed as an argument to all other classes.
#
#  FPIBG Base is a member object of all other classes. It contains the configuration file managment and error reporting.
class FPIBGBase:
    
    name = "empty"
    def __init__ (self,AppName):
        print(f"Created " + AppName)
        


    def Create(self,AppName):
        name = AppName
        log = FPIBGLog   
        log.Create(AppName)
        cfg = FPIBGConfig
        cfg.Create(AppName)

# @abstrctmethod
    def testObject(self,modNumber):
        if modNumber == 1:
            print(f"Running Mod" , modNumber , " Test")
            return
        
        print("Ivalid Module Numner")

