"""
Author: Yoni Reichert
Program name: Mini-Command-Client
Description: Sends commands and displays server responses.
Date: 06-11-2023
"""

import socket
import logging

MAX_PACKET = 1024
SERVER_ADDRESS = ('127.0.0.1', 1729)

# Set up logging
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('client')

VALID_COMMANDS = ("time", "name", "rand", "exit")


def get_message(my_socket):
    """
    Receive a message from the server socket based on a prefixed length.
    @:param my_socket: The socket object connected to the server.
    @:return: The message received from the server as a string.
    @:raises: socket.error if there's an error in receiving data.
    """
    length_str = ""
    while (char := my_socket.recv(1).decode()) != "!":
        length_str += char
    message_len = int(length_str)
    return my_socket.recv(message_len).decode()


def validate_message(message):
    """
    Validate the client's message against expected commands.
    @:param message: The message string to validate.
    @:return: True if message is valid, False otherwise.
    """
    message = message.lower()  # for easier parsing
    if message in VALID_COMMANDS:
        return True
    # if message doesn't match any command, return un-valid
    logger.info(f"User tried to enter un-valid command, ({message})")
    return False


def send_messages_to_server(client_socket):
    """
    send a message to the server and print response
    :param client_socket:
    :return:
    """
    try:
        while True:
            message = input("Enter message:")
            if message == 'exit':
                return
            # making sure the message is okay
            if validate_message(message):
                client_socket.send(message.encode())
                response = get_message(client_socket)
                print(response)
            else:
                print("You entered an un-valid message, try again or type 'exit' to exit")
    except socket.error as err:
        logger.error('Received socket error: %s', err)


def main():
    """
    Connect to the server socket, send messages, and receive responses.
    @:return: None
    @:raises: socket.error on socket-related errors.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(SERVER_ADDRESS)
        logger.info(f"Managed to connect to the server at: {SERVER_ADDRESS}")
        send_messages_to_server(client_socket)
    except socket.error as err:
        logger.error('Received socket error: %s', err)
    finally:
        client_socket.close()
        logger.info("Client socket closed.")


if __name__ == "__main__":
    assert(validate_message("time"))
    assert(not validate_message("t1m#"))
    assert(not validate_message("hello"))
    assert(validate_message("exit"))
    main()
