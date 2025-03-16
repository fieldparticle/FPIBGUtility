import os
import csv
import inspect

class DataClass:

    def __init__(self, drflag, ObjName):
        self.m_drflag = drflag
        self.data_files = []
        self.average_list = []
        self.ObjName = ObjName
       

    def Create(self, BaseObj, file_end):
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log
        self.dlvl= 1000

        
        match(file_end):
            case "PQB":
                self.topdir = self.cfg.application.testdirPQB
            case "PCD":
                self.topdir = self.cfg.application.testdirPCD
            case "DUP":
                self.topdir = self.cfg.application.testdirDUP
            case "CFB":
                self.topdir = self.cfg.application.testdirCFB
                

    def Open(self) -> bool:
            if(os.path.exists(self.topdir) == False):
                rettxt = "Data directory :" + self.topdir + " not found."
                self.bobj.log.log( 1, inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            self.ObjName,
                            self.dlvl+1,
                            rettxt)
                return False    
            
            rettxt = "Sucessfully found data directory :" + self.topdir
            self.bobj.log.log( 1, inspect.currentframe().f_lineno,
                                __file__,
                                inspect.currentframe().f_code.co_name,
                                self.ObjName,
                                0,
                                rettxt)           
            return True

    def Close(self):
        pass

    def Read(self):
        pass

    def Write(self):
        pass

    