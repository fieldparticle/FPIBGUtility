import socket
SERVER_IP = "127.0.0.1"  # Replace with the server's IP address
SERVER_PORT = 5000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
client_socket.sendall(b"Hello, server!")
data = client_socket.recv(1024)
print(f"Received from server: {data.decode()}")
client_socket.close()
