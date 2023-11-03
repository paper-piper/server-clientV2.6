import socket
MAX_PACKET = 1024
SERVER_ADDRESS = ('127.0.0.1', 1729)


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(SERVER_ADDRESS)
        message = ""
        while message != "exit":
            message = input("Enter message ")
            my_socket.send(message.encode())
            response = my_socket.recv(MAX_PACKET).decode()
            print(response)
    except socket.error as err:
        print('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == "__main__":
    main()