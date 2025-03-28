import socket
import os
import subprocess

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000
BUFFER_SIZE = 4096

#get the absolute path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to 'Particle.cfg' relative to the script directory
CONFIG_PATH = os.path.join(script_dir, '..', 'doc', 'Particle.cfg')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

#receive filename (should be 'Particle.cfg')
filename = conn.recv(1024).decode()
if not filename:
    print("No filename received.")
    conn.close()
    server_socket.close()
    exit()

print(f"Receiving file: {filename}")

#ensure the directory for CONFIG_PATH exists
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

#receive and save 'Particle.cfg'
with open(CONFIG_PATH, "wb") as f:
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        f.write(data)

print(f"File received and saved at {CONFIG_PATH}")

#Run FPIBG application with the new config
command = f"python3 {os.path.join(script_dir, '..', 'shared', 'FPIBGConfig.py')} --config {CONFIG_PATH}"
subprocess.run(command, shell=True)

conn.sendall(b"File received and FPIBG started!")

conn.close()
server_socket.close()
