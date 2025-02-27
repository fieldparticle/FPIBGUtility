import socket
import os

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
        response = self.client_socket.recv(1024)
        print(f"Server Response: {response.decode()}")

    def Write(self, ColumnName):
        """Send the configuration file to the server."""
        if not os.path.exists(self.config_file_path):
            print(f"Error: File {self.config_file_path} not found!")
            return

        filename = os.path.basename(self.config_file_path)
        #self.client_socket.sendall(filename.encode())
        #self.client_socket.send("Hello")
    def CommandLoop(self):    
            self.command = ""
            msg = ""
            while msg != "quit":
                msg = ""
                msg = input("Enter Command:")
                self.command = msg
                if msg != "quit":
                    self.Read()
                else:
                    self.command = self.command.encode('utf-8')
                    totalsent = 0
                    sent = self.client_socket.sendall(self.command)    
                    self.Close()
                    return     
                self.command = self.command.encode('utf-8')
                totalsent = 0
                sent = self.client_socket.sendall(self.command)

            #wait for response from server
            self.readData()
            self.closeConnection()
