class FPIBGLog:
    
    def __init__ (self):
        print(type(self))

    appName = "FPIBG"
    veroseLevel = 1
    debugLevel = 1

    def Create(ApplicationName):
        appName = ApplicationName
        print("Created Log File for ",appName)

    def fileObj(self) : pass

    def OpenLogFile(Name):
        fileObj = open(Name,".log","w+")
        fileObj.write("Log File Created")
        fileObj.close()

    #def w(lineNumber,functionaName,Object,ErrorCode,ErrorString):
