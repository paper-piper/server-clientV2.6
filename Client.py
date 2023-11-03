import socket
import logging

MAX_PACKET = 1024
SERVER_ADDRESS = ('127.0.0.1', 1729)

# Set up logging
logging.basicConfig(filename='client.log', level=logging.INFO)
logger = logging.getLogger('client')


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect(SERVER_ADDRESS)
        message = ""
        while message != "exit":
            message = input("Enter message: ")
            my_socket.send(message.encode())
            response = my_socket.recv(MAX_PACKET).decode()
            print(response)
        my_socket.close()
    except socket.error as err:
        logger.error('Received socket error: %s', err)
    except KeyboardInterrupt:
        logger.info("Client was terminated by the user.")
    finally:
        my_socket.close()
        logger.info("Client socket closed.")


if __name__ == "__main__":
    main()
