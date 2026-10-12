
import socket

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))

    message = "Hello from Pranaya's TCP client!"
    client.sendall(message.encode("utf-8"))

    response = client.recv(1024)
    print("Server replied:", response.decode("utf-8"))

finally:
    client.close()
