import socket
import os

class TCPIP:
    def __init__(self, server_ip="127.0.0.1", server_port=5000, buffer_size=4096):
        """Initialize the client configuration."""
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # locate the particle.cfg file
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(self.script_dir, '..', 'doc', 'Particle.cfg')

    def openConnection(self):
        """Connect to the server."""
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to server at {self.server_ip}:{self.server_port}")
        except ConnectionRefusedError:
            print("Error: Unable to connect to the server. Ensure the server is running.")
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
        self.client_socket.sendall(filename.encode())

        with open(self.config_file_path, "rb") as f:
            while True:
                data = f.read(self.buffer_size)
                if not data:
                    break
                self.client_socket.sendall(data)

        print(f"Sent file: {filename}")

        #wait for response from server
        self.readData()
        self.closeConnection()

if __name__ == "__main__":
    client = TCPIP()
    client.openConnection()
    client.writeData("Particle.cfg")
