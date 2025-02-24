import socket
import os

class TCPIP:
    def __init__(self, server_ip="10.228.15.208", server_port=50004, buffer_size=4096):
        """Initialize the client configuration."""
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # locate the particle.cfg file
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(self.script_dir, '..', 'doc', 'Particle.cfg')
        self.config_file_path = "X:\\SPRINT002MOD003\\FPIBGUtility\\Particle.cfg"

    def openConnection(self):
        """Connect to the server."""
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to server at {self.server_ip}:{self.server_port}")
        except Exception as err:
            print("Error:",err)
            exit()

    def closeConnection(self):
        """Close the client connection properly."""
        self.client_socket.close()
        print("Client connection closed.")

    def readData(self):
        """Receive confirmation message from the server."""
        response = self.client_socket.recv(1024)
        print(f"Server Response: {response.decode()}")

    def writeData(self, ColumnName):
        """Send the configuration file to the server."""
        if not os.path.exists(self.config_file_path):
            print(f"Error: File {self.config_file_path} not found!")
            return

        filename = os.path.basename(self.config_file_path)
        #self.client_socket.sendall(filename.encode())
        #self.client_socket.send("Hello")
        self.command = ""
        msg = ""
        while msg != "quit":
            msg = ""
            msg = input("Enter Command:")
            self.command = msg
            if msg != "quit":
                self.readData()
            self.command = self.command.encode('utf-8')
            totalsent = 0
            sent = self.client_socket.sendall(self.command)
            

       # with open(self.config_file_path, "rb") as f:
       #     while True:
       #        data = f.read(self.buffer_size)
       #         if not data:
       #             break
       #         self.client_socket.sendall(data)

        print(f"Sent file: {filename}")

        #wait for response from server
        self.readData()
        self.closeConnection()
