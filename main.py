import socket

MAX_PACKET = 1024
QUEUE_LEN = 1
IP = '0.0.0.0'
PORT = 1729

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    my_socket.bind((IP, PORT))
    my_socket.listen(QUEUE_LEN)
    client_socket, client_address = my_socket.accept()
    try:
        request = client_socket.recv(MAX_PACKET).decode()
        print('server received ' + request)
        client_socket.send(request.encode())
    except socket.error as err:
        print('received socket error on client socket' + str(err))
    finally:
        client_socket.close()
except socket.error as err:
    print('received socket error on server socket' + str(err))
finally:
    my_socket.close()
