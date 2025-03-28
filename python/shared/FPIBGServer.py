import socket
import os
import time
import inspect
class TCPIPServer:
    def __init__(self, ObjectName):
        self.objname = ObjectName
        

    ## Create() for the MyClass object.
    # @param   BaseObj -- (FPIBGBase) this is the glovbal class that contains the log and config file facilities.
    def Create(self,BaseObj):

        self.isConnected = False
        ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        self.log = self.bobj.log.log
        self.dlvl = 11000
        self.response = ""
        # Assign all configuration items in the create function
        # and contain them in a try block
        try:
            ## Initialize the server configuration.
            self.server_ip = self.cfg.image_server_ip
            self.server_port = self.cfg.image_server_port
            self.buffer_size = self.cfg.image_buffer_size
            self.saveimgdir = self.cfg.save_img_dir
            self.savecvsdir = self.cfg.save_csv_dir
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
        except Exception as err:
            self.bobj.log.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+1,
                err)
            self.isConnected = False

    def Open(self):
        ##Connect to the server."""
        try:
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            self.log( 0, inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                f"Image Server L:istening at {self.server_ip}:{self.server_port}")
            self.isConnected = True
        except Exception as err:
            self.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            self.isConnected = False
       
        print(f"Image Server Listening at {self.server_ip}:{self.server_port}")
        self.conn, self.addr = self.server_socket.accept()    
        
        

    def Close(self):
        """Close the server connection properly."""
        self.server_socket.close()
        print("Server connection closed.")

    def Read(self):
        #Receive confirmation message from the server.
        try:
            self.response = self.conn.recv(self.buffer_size)
        except Exception as err:
            self.log(0,   inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            self.isConnected = False
            return 
        #else
        self.log(0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                "Revc:{}{}".format(len(self.response),self.response.decode()))    

    def Write(self):
        self.command = self.command.encode('utf-8')
        try:
            self.server_socket.sendall(self.command)
        except Exception as err:
            self.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+3,
                err)
            self.isConnected = False
        #else
        self.log(0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                "Wrote:{}".format(len(self.command)))   
        
    def RecieveImgFile(self):
        # Send the send command to the server
        self.Read()

        int_array = [byte for byte in self.response]
        outdir = self.saveimgdir + self.response.decode()
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

    def RunSeriesGUI(self, OutWidget):
        self.command = "runseries"
        self.Write()
        time.sleep(1.0)
        ret = 0
        while ret == 0:
            self.Read()
            ## Instead of print send out put to OutWidget
            print(f"Server Response: {self.response.decode()}")
            msg = self.response.decode()
            msg = msg.split(",")
            if(len(msg) > 1):
                match msg[4]:
                    case "endline":
                            ## Instead of print send out put to OutWidget
                            print(f"Endline: {self.response.decode()}")    
                            self.RecieveCSVFile()
            if(msg[0] == "perfdone"):
                ret = 1
            

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
            case "sendcsv":
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
