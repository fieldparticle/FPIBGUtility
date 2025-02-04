from FPIBGLog import FPIBGLog
from FPIBGConfig import FPIBGConfig
import inspect


class FPIBGBase:
    """
    This class is the global class for all other classes

    Attributes:
        log (FPIBGLog): FPIBGLog for loogin information and errors
    """
    
    def __init__ (self,AppName):
        """
        Initializes the object with the application name.

        Args:
            AppName (string): THe Name of the application.

        
        """
        print(f"Created " + AppName)
        self.appName = AppName
    
    def Create(self):
        """
        Creates the base object and memeber objects log and config

        Args:
            self : this.
       
        """
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

    