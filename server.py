import socket
import logging
import datetime
import random

MAX_PACKET = 1024
QUEUE_LEN = 1
SERVER_ADDRESS = ('127.0.0.1', 1729)

# Set up logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('server')


def handle_messages(client_socket):
    # Handle client messages until 'exit'
    while True:
        client_input = client_socket.recv(MAX_PACKET).decode()
        if client_input.lower() == 'time':
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            client_socket.send(current_time.encode())
        elif client_input.lower() == 'name':
            client_socket.send("My name is Inigo Montoya".encode())
        elif client_input.lower() == "rand":
            random_number = str(random.randint(1, 10))
            client_socket.send(random_number.encode())
        elif client_input.lower() == 'exit':
            client_socket.close()
            return
        else:
            client_socket.send("You sent an unknown word, please try again or type 'exit' to exit.".encode())
            logger.warning("Client sent an unknown word: %s", client_input)


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(SERVER_ADDRESS)
        my_socket.listen(QUEUE_LEN)
        logger.info("Server is listening on %s:%d", SERVER_ADDRESS[0], SERVER_ADDRESS[1])
        # Handle clients forever
        while True:
            client_socket, client_address = my_socket.accept()
            try:
                logger.info("Accepted connection from %s:%d", client_address[0], client_address[1])
                handle_messages(client_socket)
            except socket.error as err:
                logger.error('Received error while handling client: %s', err)
                client_socket.close()
    except socket.error as err:
        logger.error('Received socket error on server socket: %s', err)
    except KeyboardInterrupt:
        logger.info("Server was terminated by the user.")
    finally:
        my_socket.close()
        logger.info("Server socket closed.")


if __name__ == "__main__":
    main()
