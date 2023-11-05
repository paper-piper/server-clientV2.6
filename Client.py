import socket
import logging

MAX_PACKET = 1024
SERVER_ADDRESS = ('127.0.0.1', 1729)

# Set up logging
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('client')


def get_message(my_socket):
    length_str = ""
    while (char := my_socket.recv(1).decode()) != "!":
        length_str += char
    message_len = int(length_str)
    return my_socket.recv(message_len).decode()


def validate_message(message):
    message = message.lower()  # for easier parsing
    if len(message) > 4:
        logger.error(f"Client's message too long ({len(message)})")
        return False
    if message in ("time", "name", "rand", "exit"):
        return True
    # if message doesn't match any command, return un-valid
    return False


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(SERVER_ADDRESS)
        message = ""
        while message != "exit":
            message = input("Enter message: ")
            if validate_message(message):
                my_socket.send(message.encode())
                response = get_message(my_socket)
                print(response)
    except socket.error as err:
        logger.error('Received socket error: %s', err)
    finally:
        my_socket.close()
        logger.info("Client socket closed.")


if __name__ == "__main__":
    main()
