import socket
import datetime
import random

MAX_PACKET = 1024
QUEUE_LEN = 1
SERVER_ADDRESS = ('127.0.0.1', 1729)



def handle_messages(client_socket):
    # handle client messages until exit
    while True:
        client_input = client_socket.recv(MAX_PACKET).decode()
        if client_input.lower() == 'time':
            client_socket.send(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode())
        elif client_input.lower() == 'name':
            client_socket.send("My name is inigo montoya".encode())
        elif client_input.lower() == "rand":
            client_socket.send(str(random.randint(1, 10)).encode())
        elif client_input.lower() == 'exit':
            client_socket.close()
            return
        else:
            client_socket.send("You sent an unknown word, please try again or type 'exit' to exit.".encode())
            print("client send unknown word.")


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(SERVER_ADDRESS)
        my_socket.listen(QUEUE_LEN)
        # handle clients forever
        while True:
            try:
                client_socket, client_address = my_socket.accept()
                handle_messages(client_socket)
            except socket.error as err:
                print(f'received error while handling client, ({str(err)})')
                client_socket.close()
    except socket.error as err:
        print('received socket error on server socket' + str(err))
    finally:
        my_socket.close()


if __name__ == "__main__":
    main()
