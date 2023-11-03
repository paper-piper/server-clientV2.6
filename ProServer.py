import socket
import threading

MAX_PACKET = 1024
IP = '127.0.0.1'
PORT = 1729

# List to keep track of client sockets
client_sockets = []

# Lock for managing access to clients list
lock = threading.Lock()


def handle_client(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(MAX_PACKET).decode()
            if not message:
                break
            print(f"Message from {client_address}: {message}")
            with lock:
                for other_client in client_sockets:
                    if other_client is not client_socket:
                        try:
                            other_client.send(f"{client_address}: {message}".encode())
                        except socket.error as err:
                            print(f"Error sending message to {other_client.getpeername()}: {err}")
    except socket.error as err:
        print(f"Socket error: {err}")
    finally:
        with lock:
            client_sockets.remove(client_socket)
            client_socket.close()
        print(f"Client {client_address} disconnected")

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Server listening on {IP}:{PORT}")
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            with lock:
                client_sockets.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        for cs in client_sockets:
            cs.close()
        server_socket.close()

if __name__ == "__main__":
    server()
