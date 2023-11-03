import socket

MAX_PACKET = 1024
SERVER_ADDRESS = ('127.0.0.1', 1729)

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as my_socket:
        my_socket.connect(SERVER_ADDRESS)

        while True:
            message = input("Enter message to send or type 'exit' to quit: ")
            if message.lower() == 'exit':
                break

            my_socket.send(message.encode())
            response = my_socket.recv(MAX_PACKET).decode()
            print(f"Received: {response}")


if __name__ == "__main__":
    client()
