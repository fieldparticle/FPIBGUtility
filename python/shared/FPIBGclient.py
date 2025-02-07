import socket
import os
import time

SERVER_IP = "localhost"  # localhost' if both scripts are on the same machine
SERVER_PORT = 5000
BUFFER_SIZE = 4096

#absolute path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

#path to Particle.cfg relative to the client script directory
config_file_path = os.path.join(script_dir, '..', 'doc', 'Particle.cfg')

if not os.path.exists(config_file_path):
    print(f"Error: File {config_file_path} not found!")
    exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

filename = os.path.basename(config_file_path)
client_socket.sendall(filename.encode())
time.sleep(1)  # delay to avoid merging filename & file data

#open and send file in chunks
with open(config_file_path, "rb") as f:
    while True:
        data = f.read(BUFFER_SIZE)
        if not data:
            break
        client_socket.sendall(data)

print(f"Sent file: {filename}")

#receive confirmation from server
response = client_socket.recv(1024)
print(f"Server response: {response.decode()}")

client_socket.close()
