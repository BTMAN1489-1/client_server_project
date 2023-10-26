import socket
import selectors
import enum

selector = selectors.DefaultSelector()


class KindConnect(enum.Enum):
    NEW_CONNECT = 1
    RECV_DATA = 2


def init_server(host, port):
    server_socket = socket.create_server((host, port))
    server_socket.listen()
    selector.register(server_socket, selectors.EVENT_READ, (KindConnect.NEW_CONNECT, accept_connection))


def accept_connection(client_socket):
    selector.register(client_socket, selectors.EVENT_READ, (KindConnect.RECV_DATA, recv_data))


def recv_data(client_socket, filename):
    with open(f'{filename}', "wb") as f:
        while True:
            buff = client_socket.recv(4096)
            if buff:
                f.write(buff)
            else:
                break
    selector.unregister(client_socket)
    client_socket.close()
