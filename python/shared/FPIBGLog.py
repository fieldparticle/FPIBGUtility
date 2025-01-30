from datetime import datetime

class FPIBGLog:
        
    veroseLevel = 1
    debugLevel = 1

    def __init__ (self,ApplicationName):
        self.appName = ApplicationName
        print(type(self))

   
    def Create(self):
       
        print("Created Log File for ",self.appName)

    def fileObj(self) : pass

    def Open(self):
        self.logname = self.appName + ".log"
        self.fileObj = open(self.logname,"w+")
        logstring = "{}_{}_{}:{}:{}:{}:{}:{}:{}:{}:{}\n".format("yy","mm","dd","hr","min","Application Name","ObjectName","Function Name","Line Number","ErrCode","ErrString")
        self.fileObj.write(str(logstring))  
        self.log(1,"ObjectName","Function",1,"Opened Log File Successful")
        print("Opened Log File for ",self.appName,".log")
        
        
    #Line Number:Date:24hrtime:Application:Object:Function:ErrCode:Error String
    def log(self,LineNumber,ObjectName,Function,ErrCode,ErrString):
        current_time = datetime.now()
        print(current_time.year,)
        timestr = "{}_{}_{}:{}:{}".format( current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
        logstring = "{}:{}:{}:{}:{}:{}:{}\n".format(timestr,self.appName,ObjectName,Function,LineNumber,ErrCode,ErrString)
        self.fileObj.write(str(logstring))  
        
    
    def Close(self):
        self.fileObj.close()