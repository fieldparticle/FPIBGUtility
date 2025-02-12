import configparser
import os
import libconf
import io
import inspect

class FPIBGConfig:
    def Create(self,LogObj):
        with io.open(self.configPath) as f:
            self.config = libconf.load(f)
            self.log = LogObj
            self.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            0,
                            "Test 1 Success")       

    def get_repo_root(self):
        """Gets the absolute path of the project root directory."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while not os.path.exists(os.path.join(current_dir, ".git")):
            current_dir = os.path.dirname(current_dir)
            if current_dir == "/":
                raise FileNotFoundError("Could not find .git directory")
        return current_dir
     
    def __init__(self,ObjName):
        """
        Constructor for the FPIBGConfig object.
        Saves the path of the config as a variable.
        Saves the configuration information as a dictionary.
        """
        self.ObjName = ObjName
        self.configPath = os.path.join(self.get_repo_root(), "Particle.cfg")

   


    def testObject(self,modNumber,dbglvl):
        if modNumber == 1 and dbglvl == 5:
            print(f"Running Mod" , modNumber , " Test")
            self.log.log(   inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            0,
                            "Test 1 Success")
            # Please here print out every item indicidually
            print(self.config)

        return 0
            

   
    def GetConfig(self):
        """
        Function to retreive the config object.
        This object contains all of the data from the configuration file as a dictionary.
        """
        return self.config


    