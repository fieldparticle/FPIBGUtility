import socket
import os
import time
class TCPIP:
    def __init__(self, ObjectName):
        self.objname = ObjectName
        
    ## Create() for the MyClass object.
    # @param   BaseObj -- (FPIBGBase) this is the glovbal class that contains the log and config file facilities.
    def Create(self,BaseObj):
        ## bobj contains the global object.
        self.bobj = BaseObj
        self.cfg = self.bobj.cfg.config
        """Initialize the client configuration."""
        self.server_ip = self.cfg.server_ip
        self.server_port = self.cfg.server_port
        self.buffer_size = self.cfg.server_buf_size
        self.saveimgdir = self.cfg.save_img_dir
        self.savecvsdir = self.cfg.save_csv_dir
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Open(self):
        """Connect to the server."""
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to server at {self.server_ip}:{self.server_port}")
        except Exception as err:
            print("Error:",err)
            exit()

    def Close(self):
        """Close the client connection properly."""
        self.client_socket.close()
        print("Client connection closed.")

    def Read(self):
        """Receive confirmation message from the server."""
        self.response = self.client_socket.recv(self.buffer_size)
        print(f"Server Response: {self.response.decode()}")

    def Write(self, ColumnName):
        """Send the configuration file to the server."""
        if not os.path.exists(self.config_file_path):
            print(f"Error: File {self.config_file_path} not found!")
            return
        
    def RecieveCSVFile(self):
        # Send the send command to the server
        self.command = self.command.encode('utf-8')
        sent = self.client_socket.sendall(self.command)
        #Read the number of blocks
        self.Read()
        int_array = [byte for byte in self.response]
        print(int_array)
        outdir = self.savecvsdir + "/perfdataPQB/0000CollisionDataSetTESTXTEST.csv"
        f = open(outdir, "w")
        for i in range(int_array[0]):
            self.response = self.client_socket.recv(self.buffer_size)
            f.writelines(self.response.decode())

    def RecieveImgFile(self):
        # Send the send command to the server
        self.command = self.command.encode('utf-8')
        sent = self.client_socket.sendall(self.command)
        #Read the number of blocks
        self.Read()
        int_array = [byte for byte in self.response]
        outdir = self.saveimgdir + "/file001.png"
        f = open(outdir, "wb")
        for i in range(int_array[0]):
            self.response = self.client_socket.recv(self.buffer_size)
            f.write(self.response)

    def RunLoop(self):
        self.command = "runseries"
        self.command = self.command.encode('utf-8')
        sent = self.client_socket.sendall(self.command)    
        time.sleep(1.0)
        ret = 0
        while ret == 0:
            self.response = self.client_socket.recv(self.buffer_size)
            print(f"Server Response: {self.response.decode()}")
            msg = self.response.decode();
            msg = msg.split(",")
            match msg[0]:
                case "quit":
                    ret = 1;
                case "perfline":
                    self.response = self.client_socket.recv(self.buffer_size)
                    print(f"Server Response: {self.response.decode()}")
                case "endline":
                    ret = 1
            time.sleep(1.0)

    def CommandLoop(self):    
            self.command = ""
            msg = ""
            while msg != "quit":
                msg = ""
                msg = input("Enter Command:")
                self.command = msg
                match msg:
                    case "quit":
                        self.command = self.command.encode('utf-8')
                        totalsent = 0
                        sent = self.client_socket.sendall(self.command)    
                        self.Close()
                        return
                    case "sendcsv":     
                        self.RecieveCSVFile()
                    case "sendimg":     
                        self.RecieveImgFile()
                    case "test": 
                        self.command = self.command.encode('utf-8')
                        sent = self.client_socket.sendall(self.command)
                        self.Read()
                    case "runseries":
                        self.RunLoop()
                              
            self.closeConnection()
