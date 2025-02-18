from FPIBGLog import FPIBGLog
from FPIBGConfig import FPIBGConfig
import inspect


## MyClass is a class to act an an example of our stye and formating guide.
class MyClass:

    ##  Constructor for the MyClass object.
    # @param   ObjName --  (string) Saves the name of the object.
    def __init__(self,ObjName):
        ## ObjName contains the name of this object.
        self.ObjName = ObjName

    ## Create() for the MyClass object.
    # @param   BaseObj -- (FPIBGBase) this is the glovbal class that contains the log and config file facilities.
    def Create(self,BaseObj):
        ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        
    ##  Performs opening of file and communcations and takes no input. Any data this function needs 
    #    is assigned to class members in the Create function
    #  @param self The object pointer.
    def Open(self):
        pass

    ##  Performs closing of files and communcations and takes no input.
    #  @param self The object pointer.
    def Close(self):
        pass

    ##  Performs reading of files and communcations. 
    #  @param self The object pointer.
    def Read(self):
        pass
    
    ##  Write() performs writing to files and communcations.
    #  @param self The object pointer.
    def Write(self):
        pass

    
    ## This function performs mod tests. It is not only a test function but provides an example of how you class
    # works to other developers. The first test should be as shown here, that is to test access to logging and 
    # configuration.
    # @param modNumber
    #   (int) the module number of the test.
    # @param dbglvl 
    #   (int) the debug verobosity ranges from 0 to 5. Where 0 is do not perform the test and no output 
    #   and 5 which is the greatest amount of output.
    def testObject(self,modNumber,dbglvl):
        if modNumber == 1 and dbglvl == 5:
            print(f"Running Mod" , modNumber , " Test")
            self.bobj.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            0,
                            "Test 1 Success")
            self.bobj.cfg.testObject(modNumber,dbglvl)
            print(self.cfg.application.window.title)
            
            return 0
