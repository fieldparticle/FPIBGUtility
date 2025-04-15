import socket
import os
import time
import inspect
from PyQt6.QtCore import Qt,QRect,QObject,QThread, pyqtSignal

class TCPIPClient:
    
    def __init__(self, ObjectName):
        self.objname = ObjectName
        self.Text = "";
    
    def rptError(self,err,control):
         s = "Error {0}".format(str(err)) 
         self.redText(control)
        
    def redText(self,msg,control) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:red;\" >"
        Txt += msg
        Txt += "</span>"
        control.append(Txt)
        control.update()

    def greenText(self,msg,control) :
        Txt = "<span style=\" font-size:8pt; font-weight:600; color:green;\" >"
        Txt += msg
        Txt += "</span>"
        control.append(Txt)
        control.update()

    def getText(self):
        return self.Text
    
    def CreateGUI(self,BaseObj,control):
        if(self.Create(BaseObj) == 0):
            self.greenText( self.Text,control)
        else:
            self.redText( self.Text,control)  
        
    ## Create() for the MyClass object.
    # @param   BaseObj -- (FPIBGBase) this is the glovbal class that contains the log and config file facilities.
    def Create(self,BaseObj):

        self.isConnected = False
        ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.dlvl = 2000
        # Assign all configuration items in the create function
        # and contain them in a try block
        try:
            ## Initialize the client configuration.
            self.server_ip = self.cfg.server_ip
            self.server_port = self.cfg.server_port
            self.buffer_size = self.cfg.server_buf_size
            self.saveimgdir = self.cfg.save_img_dir
            self.savecvsdir = self.cfg.save_csv_dir
           
            self.Text =  f"Created client successfully {self.server_ip}:{self.server_port}"
            return 0
        except Exception as err:
            self.bobj.log.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+1,
                err)
            self.isConnected = False
            return 1
        
    def OpenGUI(self,control):
        self.Open()

    def OpenAdd(self, server_ip,server_port): 
        self.server_ip = server_ip
        self_server_port = server_port
        self.Open()

    def Open(self): 
        ##Connect to the server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            
            self.client_socket.connect((self.server_ip, self.server_port))
            self.log( 0, inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                f"Connected to server at {self.server_ip}:{self.server_port}")
            self.Text = f"Connected to server at {self.server_ip}:{self.server_port}"
            self.isConnected = True
            
            return 0
        except Exception as err:
            self.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            s = "Error {0}".format(str(err)) 
            self.Text = s
            self.isConnected = False
            return 1

    def CloseGUI(self,control):
        self.client_socket.close()
        self.isConnected = False
        self.greenText("Closed Session",control)

    def Close(self):
        """Close the client connection properly."""
        self.client_socket.close()
        self.isConnected = False
        self.client_socket.close()
        self.Text = "Client Connection Closed."
        print("Client connection closed.")

    def Read(self):
        #Receive confirmation message from the server.
        try:
            self.response = self.client_socket.recv(self.buffer_size)
            self.Text = self.response.decode()
            return 0
        except Exception as err:
            self.log(0,   inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            self.isConnected = False

    def ReadBlk(self,size):
        #Receive confirmation message from the server.
        try:
            self.response = self.client_socket.recv(size)
            self.Text = self.response.decode()
            return 0
        except Exception as err:
            self.log(0,   inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            self.isConnected = False
            return 1

    def ReadGUI(self,control):
        #Receive confirmation message from the server.
        try:
            self.response = self.client_socket.recv(self.buffer_size)
            self.greenText(self.response.decode(),control)
            self.response = ""
            return 0
        except Exception as err:
            self.log(0,   inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            self.isConnected = False
            self.redText(self.response.decode(),control)
            self.response = ""
            return 1
        
    def Write(self):
        self.command = self.command.encode('utf-8')
        try:
            self.client_socket.sendall(self.command)
            self.Text = "Successful Write"
#            print("write {}".format(self.command) )
            return 0
        except Exception as err:
            self.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+3,
                err)
            self.isConnected = False
            s = "Error {0}".format(str(err)) 
            self.Text = s
            return 1

      
    
    def WriteCmd(self,CMD):
        self.command = CMD
        return self.Write()
    
    def WriteGUI(self,msg,control):
        self.command = msg
        self.command = self.command.encode('utf-8')
        try:
            self.client_socket.sendall(self.command)
            return 0
        except Exception as err:
            self.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+3,
                err)
            self.isConnected = False
            s = "Error {0}".format(str(err)) 
            self.Text = s
            self.redText(control)
            return 1

        #else
        self.log(0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                 "Wrote:{} for {} bytes".format(msg,len(self.command)))   
        self.Text = "Wrote:{} for {} bytes".format(msg,len(self.command))
        self.greenText(self.Text,control)
        return 0
   
    def RecieveCSVFile(self):
        #Read the number of blocks, type of report file, and filename
        self.Read()
        msg = self.response.decode()
        msg = msg.split(",")
        match msg[0]:
            case "1":         
                outdir = self.savecvsdir + "/perfdataPQB/" + msg[2]
                self.Text = "Recieving {}".format(outdir)
            case "perfdone":
                return 1
        blks = int(msg[1])
        print(outdir)
        try:
            f = open(outdir, "w")
        except Exception as err:
            self.bobj.log.log(   inspect.currentframe().f_lineno,
                    __file__,
                    inspect.currentframe().f_code.co_name,
                    self.objname,
                    self.dlvl+4,
                    err)
            s = "Error {0}".format(str(err)) 
            self.Text = s
            print("File not Saved" + err )
            return 
        #else
        self.log( 0, inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                "Opened:" + outdir)   

        for i in range(blks):
            self.response = self.client_socket.recv(self.buffer_size)
            wline = self.response.decode();
            modified_lines = [line.rstrip('\r\x00') for line in wline]
            f.writelines(modified_lines)
        return 0

    
    def RecieveImgFile(self):
        # Send the send command to the server
        self.Wrtie()
        self.Read()
        int_array = [byte for byte in self.response]
        outdir = self.saveimgdir + "/file001.png"
        print(outdir)
        f = open(outdir, "wb")
        for i in range(int_array[0]):
            self.Read()
            f.write(self.response)

    def RecieveImgFileGUI(self,OutWidget):
        # Send the send command to the server
        self.Write()
        #Read the number of blocks
        self.Read()
        ## Instead of print send out put to OutWidget
        print("Recieved.  {len(self.response)}  Bytes")
        int_array = [byte for byte in self.response]
        outdir = self.saveimgdir + "/file001.png"
        ## Instead of print send out put to OutWidget
        print(outdir)
        f = open(outdir, "wb")
        for i in range(int_array[0]):
            self.Read()
            f.write(self.response)

    def RunSeriesGUI(self, control,tab):
        self.command = "runseries"
        self.greenText("Sending:runseries",control)
        self.WriteGUI(self.command,control)
        tab.update()
        ret = 0
        while ret == 0:
            ret = self.ReadBlk(1024)
            txt = f"Server Response: {self.response.decode()}"
            self.greenText(txt,control)
            

    def RecieveCSVFileGUI(self,control):
        #Read the number of blocks, type of report file, and filename
        self.Read()
        msg = self.response.decode();
        msg = msg.split(",")
        match msg[1]:
            case "1":         
                outdir = self.savecvsdir + "/perfdataPQB/" + msg[2]
        blks = int(msg[0])
        try:
            f = open(outdir, "w")
        except Exception as err:
            self.bobj.log.log(   inspect.currentframe().f_lineno,
                    __file__,
                    inspect.currentframe().f_code.co_name,
                    self.objname,
                    self.dlvl+4,
                    err)
            print("File not Saved" + err )
            s = "Error {0}".format(str(err)) 
            self.Text = s
            self.redText(control)
            return 
        #else
        self.log( 0, inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                "Opened:" + outdir)   

        for i in range(blks):
            self.response = self.client_socket.recv(self.buffer_size)
            wline = self.response.decode();
            modified_lines = [line.rstrip('\r\x00') for line in wline]
            f.writelines(modified_lines)

    def RunSeriesCMD(self):
        self.command = "runseries"
        self.Write()
        time.sleep(1.0)
        ret = 0
        while ret == 0:
            self.Read()
            print(f"Server Response: {self.response.decode()}")
            msg = self.response.decode()
            msg = msg.split(",")
            if(len(msg) > 1):
                match msg[4]:
                    case "endline":
                            print(f"Endline: {self.response.decode()}")    
                            self.RecieveCSVFile()
            if(msg[0] == "perfdone"):
                ret = 1
                      
            time.sleep(1.0)

    def SendCommandGUI(self,msg):
          match msg:
            case "quit":
                self.Write()
                self.Close()
                return
            case "sndcsv":
                self.Write()
                self.RecieveCSVFile()
            case "sendimg":     
                self.RecieveImgFile()
            case "test": 
                self.Write()
                self.Read()
            case "runseries":
                self.RunLoop()


    def CommandLoop(self):    
            self.command = ""
            msg = ""
            while msg != "quit":
                msg = ""
                msg = input("Enter Command:")
                self.command = msg
                match msg:
                    case "quit":
                        if (self.isConnected == True):
                            self.Write()
                            self.Close()
                            return
                        return;
                    case "sndcsv":
                        self.Write()
                        self.RecieveCSVFile()
                    case "sndimg":     
                        self.RecieveImgFile()
                    case "test": 
                        self.Write()
                        self.Read()
                    case "rnser":
                        self.RunSeriesCMD()
                              
            self.closeConnection()
