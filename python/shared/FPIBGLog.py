from datetime import datetime
import inspect
import os

## FPIBGLog class perfomrs formmated logging for all other classes
class FPIBGLog:
        
    ##  FPIBGLog Constructor.
    # @param   ApplicationName --  (string) Passes the name of the calling application.
    def __init__ (self,ApplicationName):
        self.appName = ApplicationName
        print(type(self))
        

    def CheckLogFile(self,ErrString)-> bool:
        self.Close()
        ret = 0;
        self.FileObj = open(self.logName, "r")
        for line in self.FileObj:
            if ErrString in line:
                print(line)
                return True
        return False    
    


    ## Standard create for the log class object.
    # @param   LogName -- (string) the name of the log file which will be written to.
    def Create(self,LogName):
        self.logName = LogName
        print("Created Log File for ",self.appName)

    def fileObj(self) : pass

    ## This function opens the log file and writes the title header to the log file.
    # The format is:
    # yy,mm,dd,hr,min,application,class,function,object,line number,error code, and error string.
    # 
    def Open(self):
        self.fileObj = open(self.logName,"w+")
        logstring = "{},{}_{}_{}:{}:{},{},{},{},{},{},{},{}\n".format("lvl",
                                                                    "yy",
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
        self.log(1,inspect.currentframe().f_lineno,
                            __file__,
                            inspect.currentframe().f_code.co_name,
                            "LogObject",
                            0,
                            "Opened Logfile success")
        print("Opened Log File for FPIBG.log")
        
    def logs(self,classObj,ErrString):
        current_time = datetime.now()       
        timestr = "{}_{}_{}:{}:{}".format( current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
        logstring = "{},{}\n".format(classObj.ObjName,ErrString)
        self.fileObj.write(str(logstring))  
        self.fileObj.flush()

    ## Write the log item to the log file.
    # @param Line number from import inspect.currentframe().f_lineno
    # @param ClassName from the "__file__" reserved python keyword.
    # @param Object name from the inspect.currentframe().f_code.co_name
    # @param The function name enterred as a string.
    # @param The Object Name from self.ObjName.
    # @param The error code from list to be determined later. Just pass 0 for success and 1 for failure.
    # @param The error text.
    def log(self,lvl,LineNumber,ClassName,Function,ObjName,ErrCode,ErrString):
        if(lvl <= lvl):
            current_time = datetime.now()       
            timestr = "{}_{}_{}:{}:{}".format( current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
            logstring = "{},{},{},{},{},{},{},{},{}\n".format(lvl,timestr,self.appName,os.path.basename(ClassName),Function,LineNumber,ObjName,ErrCode,ErrString)
            self.fileObj.write(str(logstring))  
            self.fileObj.flush()
    ## Standard close. Closes the log file.
    def Close(self):
        self.fileObj.close()