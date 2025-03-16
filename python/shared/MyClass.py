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
    # \param BaseObj -- (FPIBGBase) this is the global class that contains the log and config file facilities.
    def Create(self,BaseObj):
        ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        # Assign this objects debug level
        self.dlvl = 50
        
    ##  Performs opening of file and communcations and takes no input. Any data this function needs 
    #    is assigned to class members in the Create function
    #  @param self The object pointer.
    def Open(self):
        pass

    ##  Close(self) Performs closing of files and communcations and takes no input.
    #  @param self The object pointer.
    def Close(self):
        self.bobj.Close()
        pass

    ## Read(). Performs reading of files and communcations. 
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
    # @param modName
    #   (string) the module name of the test.
   
    def testObject(self,modName):
        if(modName == "Test Get All Config Items"):
            print(f"Running Mod" + modName)
            self.bobj.log.log( 1,  inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            0,
                            f"Running Mod:" + modName)
            self.bobj.cfg.testObject(modName)
            print(self.cfg.application.window.title)

        if(modName == "Log an Error"):
            print(f"Running Mod" + modName)
            self.bobj.log.log( 1,  inspect.currentframe().f_lineno,
                        __file__,
                        inspect.currentframe().f_code.co_name,
                        self.ObjName,
                        self.dlvl+1,
                        f"Running Mod:" + modName)
                
        
        return 0
