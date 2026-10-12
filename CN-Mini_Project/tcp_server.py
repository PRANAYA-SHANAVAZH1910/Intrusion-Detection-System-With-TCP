
import socket
from event_logger import log_event

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"TCP server listening on {HOST}:{PORT}")

try:
    while True:
        conn, addr = server.accept()

        with conn:
            source_ip = addr[0]
            destination_ip, destination_port = conn.getsockname()

            log_event(
                source_ip=source_ip,
                destination_ip=destination_ip,
                destination_port=destination_port,
                event_type="connection_accepted",
                status="success"
            )

            data = conn.recv(1024)

            if data:
                print("Client says:", data.decode("utf-8"))
                conn.sendall(
                    b"Message received successfully!"
                )

finally:
    server.close()
