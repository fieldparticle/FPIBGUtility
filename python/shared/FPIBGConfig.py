import configparser
import os
import libconf
import io
import inspect

class FPIBGConfig:
    def Create(self,LogObj,CfgFileName):
        self.CfgFileName = CfgFileName
        self.configPath = os.path.join(self.get_repo_root(), self.CfgFileName)
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
        

    def Open():
        pass
    def Close():
        pass    

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
            print(self.config.application.window.title)
            print(self.config.application.window.size.w)
            print(self.config.application.window.size.h)
            print(self.config.application.frame_delay)
            print(self.config.application.end_frame)
            print(self.config.application.dt)
            print(self.config.application.cap_name)
            print(self.config.application.cap_num)
            print(self.config.application.cap_frames)
            print(self.config.application.framesBuffered)
            print(self.config.application.shader_out)
            print(self.config.application.frag_kernParticle)
            print(self.config.application.frag_kernParticlespv)
            print(self.config.application.vert_kernParticle)
            print(self.config.application.vert_kernParticlespv)
            print(self.config.application.comp_kernParticle)
            print(self.config.application.comp_kernParticlespv)
            print(self.config.application.doAuto)
            print(self.config.application.doAutoWait)
            print(self.config.application.testfile)
            print(self.config.application.perfTest)
            print(self.config.application.testdirPQB)
            print(self.config.application.testdirCFB)
            print(self.config.application.testdirPCD)
            print(self.config.application.testdirDUP)
            print(self.config.application.compileShaders)
            print(self.config.application.enableValidationLayers)
            print(self.config.application.stopondata)
            print(self.config.application.debugLevel)
            print(self.config.application.reportCompFramesLessThan)
            print(self.config.application.reportGraphFramesLessThan)
            print(self.config.application.framesInFlight)
            for x in self.config.application.device_extensions:
                print(x)
            for x in self.config.application.instance_extensions:
                print(x)
            for x in self.config.application.validation_layers:
                print(x)
            print(self.config.application.printExtension)
            print(self.config.application.printDevLimtits)
            print(self.config.application.verbose_rpt)



        return 0
            

   
    def GetConfig(self):
        """
        Function to retreive the config object.
        This object contains all of the data from the configuration file as a dictionary.
        """
        return self.config


    