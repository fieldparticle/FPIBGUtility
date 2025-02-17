from datetime import datetime
import inspect
class FPIBGLog:
        
    veroseLevel = 1
    debugLevel = 1

    def __init__ (self,ApplicationName):
        self.appName = ApplicationName
        print(type(self))

   
    def Create(self,LogName):
        self.logName = LogName
        print("Created Log File for ",self.appName)

    def fileObj(self) : pass

    def Open(self):
        
        self.fileObj = open(self.logName,"w+")
        logstring = "{}_{}_{}:{}:{}:{}:{}:{}:{}:{}:{}:{}\n".format("yy",
                                                                   "mm",
                                                                   "dd",
                                                                   "hr",
                                                                   "min",
                                                                   "Application Name",
                                                                   "ClassName",
                                                                   "Function Name",
                                                                   "ObjName",
                                                                   "Line Number",
                                                                   "ErrCode",
                                                                   "ErrString")
        self.fileObj.write(str(logstring))  
        self.log(inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            "LogObject",
                            0,
                            "Opened Logfile success")
        print("Opened Log File for FPIBG.log")
        
        
    #Line Number:Date:24hrtime:Application:Object:Function:ErrCode:Error String
    def log(self,LineNumber,ClassName,Function,ObjName,ErrCode,ErrString):
        current_time = datetime.now()       
        timestr = "{}_{}_{}:{}:{}".format( current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
        logstring = "{}:{}:{}:{}:{}:{}:{}:{}\n".format(timestr,self.appName,ClassName,Function,LineNumber,ObjName,ErrCode,ErrString)
        self.fileObj.write(str(logstring))  
        
    
    def Close(self):
        self.fileObj.close()