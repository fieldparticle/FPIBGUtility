from datetime import datetime
import os
from os import walk

class pptimg2md:
        
    veroseLevel = 1
    debugLevel = 1

    def __init__ (self,InputDirectory, OutputFile):
        self.InputDirectory = InputDirectory;
        self.OutputFile = OutputFile;
        print(type(self))

   
    def Create(self):
       pass
        

    def fileObj(self) : pass

    def Open(self):
        # Get the list of all files and directories
        dir_list = os.listdir(self.InputDirectory )
        dir_list.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        self.fileObj = open(self.OutputFile,"w+")
        
        for x in dir_list:
            mdstring = "![alt text]({})\r\n".format(x)
            self.fileObj.write(str(mdstring))  
            
        self.Close()
  
    
    def Close(self):
        self.fileObj.close()