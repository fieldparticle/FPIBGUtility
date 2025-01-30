from FPIBGLog import FPIBGLog
from FPIBGConfig import FPIBGConfig
import inspect


## FPBIG Base class. This class is passed as an argument to all other classes.
#
#  FPIBG Base is a member object of all other classes. It contains the configuration file managment and error reporting.
class FPIBGBase:
    
    name = "empty"
    def __init__ (self,AppName):
        print(f"Created " + AppName)
        self.appName = AppName


    def Create(self):
        self.log = FPIBGLog(self.appName)   
        self.log.Create()
        self.log.Open()
        self.cfg = FPIBGConfig
        #self.cfg.Create( )
        

# @abstrctmethod
    def testObject(self,modNumber):
        if modNumber == 1:
            print(f"Running Mod" , modNumber , " Test")
            self.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            0,
                            "Test 1 Success")
            return
        
        self.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            1,
                            "Invalid test number")

    def Open(self):
        self.log.Open()
    def Close(self):
        self.log.Close()