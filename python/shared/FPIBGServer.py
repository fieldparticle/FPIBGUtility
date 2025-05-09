import socket
import os
import time
import inspect
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
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
        self.Text = ""
        
        # Assign all configuration items in the create function
        # and contain them in a try block
        try:
            ## Initialize the server configuration.
            self.server_ip = self.cfg.image_server_ip
            self.server_port = self.cfg.image_server_port
            self.buffer_size = self.cfg.image_buffer_size
            self.saveimgdir = self.cfg.save_img_dir
            self.savecvsdir = self.cfg.save_csv_dir
            
            return 0
        except Exception as err:
            self.bobj.log.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+1,
                err)
            s = "Error {0}".format(str(err)) 
            self.Text = s
            self.isConnected = False
            return 1
        
    def Open(self):
        ##Connect to the server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Text =  f"Created Image Server successfully {self.server_ip}:{self.server_port}"
            self.server_socket.bind((self.server_ip, self.server_port))
            self.server_socket.listen(1)
            self.log( 0, inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                f"Image Server L:istening at {self.server_ip}:{self.server_port}")
            self.Text = f"Image Server L:istening at {self.server_ip}:{self.server_port}"
            self.isConnected = True
    
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
            return 1;
    
        print(f"Image Server Listening at {self.server_ip}:{self.server_port}")
        self.Text = f"Image Server Listening at {self.server_ip}:{self.server_port}"
        return 0;    
        
    def Accept(self):
        self.conn, self.addr = self.server_socket.accept()    
        

    def Close(self):
        """Close the server connection properly."""
        self.server_socket.close()
        print("Server connection closed.")

    def readnbyte(self, n):
        buff = bytearray(n)
        pos = 0
        while pos < n:
            cr = self.conn.recv_into(memoryview(buff)[pos:])
            if cr == 0:
                raise EOFError
            pos += cr
        return buff
    
    def Read(self):
        #Receive confirmation message from the server.
        try:
            self.response = ""
            self.response = self.conn.recv(self.buffer_size)
        except Exception as err:
            self.log(0,   inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            s = "Error {0}".format(str(err)) 
            self.Text = s
            print(s)
            self.isConnected = False
            return 
        #else
        
        
    def ReadBuf(self, bufsize):
         #Receive confirmation message from the server.
        try:
            return self.conn.recv(bufsize)
        except Exception as err:
            self.log(0,   inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+2,
                err)
            s = "Error {0}".format(str(err)) 
            self.Text = s
            print(s)
            self.isConnected = False
            return ""
        #else
       

    def Write(self):
        self.command = self.command.encode('utf-8')
        try:
            self.conn.sendall(self.command)
        except Exception as err:
            self.log( 0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                self.dlvl+3,
                err)
            s = "Error {0}".format(str(err)) 
            self.Text = s
            print(s)
            self.isConnected = False
        #else
        self.log(0,  inspect.currentframe().f_lineno,
                __file__,
                inspect.currentframe().f_code.co_name,
                self.objname,
                0,
                "Wrote:{}".format(len(self.command)))   
        
    def RecieveBMPFile(self):
        buffer =  BytesIO()    
        self.command = "start"
        self.Write()
        msg = self.Read()
        msg = self.response
        msg = msg.decode()
        msg = msg.split(",")
        if(msg[0] == "end"):
            print("Got end msg")
            return 1;
        self.Text ="File:{},block1:{},block 2{},file size{}".format(msg[0],msg[1],msg[2],msg[3])
        print(self.Text)
        outdir = self.saveimgdir + "/" + msg[0]
        #f = open(outdir, "wb")
        
        block1 = int(msg[1])
        block2 = int(msg[2])
        block3 = int(msg[3])
        self.command = "next"
        self.Write()

        blk1 = self.ReadBuf(block1)
        buffer.write(blk1)

        self.command = "next"
        self.Write()
        #f.write(self.response)
        blk2 = self.ReadBuf(block2)

        #f.write(blk2)
        self.command = "next"
        self.Write()
        buffer.write(blk2)
        
        bytes = self.readnbyte(block3)
        #blk3 = self.ReadBuf(block3)
        print("Total Bytes{}".format(block3))
        #f.write(blk3)
        buffer.write(bytes)
        
       
        #f.close()
        self.im = Image.open(buffer)
        #im = Image.frombuffer(buffer)
        self.im.save("img.bmp")
        del buffer
        #plt.imshow(im)
        #plt.show()
        return 0


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
