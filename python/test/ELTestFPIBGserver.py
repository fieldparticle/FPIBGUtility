import socket
import os
import subprocess

HOST = "127.0.0.1"  # listen on localhost
PORT = 50004
BUFFER_SIZE = 4096

# get the absolute path to the directory containing this script (test/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# config file is stored outside `test/`, in the main directory
CONFIG_PATH = os.path.join(script_dir, "..", "ELParticle.cfg") # Particle file * * *

# create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"server listening on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"connected by {addr}")

    try:
        while True:  # keep connection open for multiple commands
            # receive the initial message
            data = conn.recv(1024).decode().strip()  # strip to remove unwanted spaces or newlines
            if not data:
                print("client disconnected.")
                break  # exit loop when client disconnects

            if data.endswith(".cfg"):  
                # if it's a file, receive and save it
                print(f"receiving file: {data}")

                with open(CONFIG_PATH, "wb") as f:
                    while True:
                        file_data = conn.recv(BUFFER_SIZE)
                        if not file_data:
                            break
                        f.write(file_data)

                print(f"file received and saved at {CONFIG_PATH}")

                # run FPIBG application with the new config
                command = f"python3 {os.path.join(script_dir, '..', 'shared', 'FPIBGConfig.py')} --config {CONFIG_PATH}"
                subprocess.run(command, shell=True)

                conn.sendall(b"file received and FPIBG started!")
            
            else:
                # if it's a normal command, handle it
                print(f"received command: {data}")
                conn.sendall(f"command '{data}' received!".encode())

    except Exception as e:
        print(f"error: {str(e)}")

    conn.close()
