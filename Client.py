import socket
MAX_PACKET = 1024
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    my_socket.connect(('127.0.0.1', 1729))

    my_socket.send('hello world'.encode())

    response = my_socket.recv(MAX_PACKET).decode()
except socket.error as err:
    print('received socket error ' + str(err))
finally:
    my_socket.close()
