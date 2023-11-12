"""
Author: Yoni Reichert
Program name: Mini-Command-Server
Description: Listens for commands and sends back dynamic responses.
Date: 06-11-2023
"""

import socket
import logging
import datetime
import random

MAX_PACKET = 1024
QUEUE_LEN = 1
SERVER_ADDRESS = ('0.0.0.0', 1729)

# Set up logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('server')


def handle_message(message):
    if message == 'time':
        response = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    elif message == 'name':
        response = "My name is Inigo Montoya"
    elif message == "rand":
        response = str(random.randint(1, 10))
    else:
        logger.error("Client sent unknown word")
        response = "You sent an unknown command, try again or type 'exit' to exit"
    # server doesn't need to check to un-valid message since client is responsible for checking

    response = str(len(response)) + "!" + response
    return response


def handle_client(client_socket):
    """
    Handle client messages until 'exit' command is received.
    @:param client_socket: The socket object associated with the client.
    @:return: None
    @:raises: socket error if there's an error in receiving data.
    """

    while True:
        client_input = client_socket.recv(4).decode()
        if client_input.lower() == 'exit':
            client_socket.send("6!exited".encode())
            client_socket.close()
            return
        response = handle_message(client_input.lower())
        client_socket.send(response.encode())


def main():
    """
    Initialize the server socket, accept incoming connections, and handle messages.
    @:return: None
    @:raises: socket.error on socket-related errors, KeyboardInterrupt when user interrupts the process.
    """
    assert len(handle_message("time")) == 22
    assert 0 < int(handle_message("rand")[2]) < 10
    assert handle_message("name") == "24!My name is Inigo Montoya"
    assert len(handle_message("invalid message")) == 64
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.bind(SERVER_ADDRESS)
        my_socket.listen(QUEUE_LEN)
        logger.info(f"Server is listening on {SERVER_ADDRESS[0]}: {SERVER_ADDRESS[1]}")
        # Handle clients forever
        while True:
            client_socket, client_address = my_socket.accept()
            try:
                logger.info(f"Accepted connection from {client_address[0]}: {client_address[1]}")
                handle_client(client_socket)
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
