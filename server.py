"""
Author: Yoni Reichert
Program name: Mini-Command-Server
Description: Listens for commands and sends back dynamic responses.
Date: 06-11-2023
"""

import glob
import socket
import logging
import os
import shutil
import subprocess
import pyautogui

MAX_PACKET = 1024
QUEUE_LEN = 1
SERVER_ADDRESS = ('0.0.0.0', 1729)

# Set up logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('server')


def process_request(msg_type, msg_cont):
    """
    process client's command into server's response
    :param msg_type:
    :param msg_cont:
    :return:
    """
    response = ""
    match msg_type:
        case 0:
            pass
        # continue for all cases
        case _:
            logger.error("Client sent unknown word")
            response = "You sent an unknown command, try again or type 'exit' to exit"
    response = str(len(response)) + "!" + msg_type + response
    return response


def parse_message(sock):
    """
    Receives messages from the server.
    :param sock:
    :return:
    Messages protocol:
    since message type is fixed (0-9) a separation symbol is not required
    [message content length]![message type][message content]
    0. Exit
    1. ...

    """
    len_str = ""
    while (char := sock.recv(1).decode()) != "!":
        len_str += char
    msg_len = int(len_str)
    msg_type = int(sock.recv(1).decode())
    msg_content = sock.recv(msg_len).decode()
    return msg_type, msg_content


def handle_client_messages(client_socket):
    """
    Handle client messages until 'exit' command is received.
    also contains all the function for the different server commands
    @:param client_socket: The socket object associated with the client.
    @:return: None
    @:raises: socket error if there's an error in receiving data.
    """
    while True:
        msg_type, msg_cont = parse_message(client_socket)
        response = process_request(msg_type, msg_cont)
        client_socket.send(response.encode())


def accept_client(server_socket):
    """
    accept client and get his messages until disconnected
    :param server_socket:
    :return:
    """
    client_socket, client_address = server_socket.accept()
    try:
        logger.info(f"Accepted connection from {client_address[0]}: {client_address[1]}")
        handle_client_messages(client_socket)
    except socket.error as err:
        logger.error('Received error while handling client: %s', err)
        client_socket.close()


def main():
    """
    Initialize the server socket, accept incoming connections, and handle messages.
    @:return: None
    @:raises: socket.error on socket-related errors, KeyboardInterrupt when user interrupts the process.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Starting server
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen(QUEUE_LEN)
        logger.info(f"Server is listening on {SERVER_ADDRESS[0]}: {SERVER_ADDRESS[1]}")
        # listen to clients forever
        while True:
            accept_client(server_socket)
    except socket.error as err:
        logger.error('Received socket error on server socket: %s', err)
    except KeyboardInterrupt:
        logger.info("Server was terminated by the user.")
    finally:
        server_socket.close()
        logger.info("Server socket closed.")


def dir_cmd(path):
    return glob.glob(path + r"\*.*")


def delete_cmd(path):
    try:
        os.remove(path)
        return True
    except:
        return False


def copy_cmd(copy_from, copy_to):
    try:
        shutil.copy(copy_from,copy_to)
        return True
    except:
        return False


def execute_cmd(path):
    try:
        subprocess.call(path)
        return True
    except:
        return False


def take_screenshot_cmd():



if __name__ == "__main__":
    pass
    # Make new assertion checks
    # main()
