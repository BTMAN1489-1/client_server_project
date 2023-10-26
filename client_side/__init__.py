import socket
import os
from client_side.misc import StatusCode


class ClientSocket:
    connection = None
    _instance = None

    def __new__(cls, host: str, port: int):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._instance.port = port
        cls._instance.host = host
        return cls._instance

    def create_connection(self):
        try:
            self.connection = socket.create_connection((self.host, self.port), timeout=2*60)
            recv = self.connection.recv(4096).decode('UTF-8')
            print(recv)
            if recv != 'OK':
                raise socket.error()
        except socket.error:
            return StatusCode.FAILED_CONNECTION
        else:
            return StatusCode.SUCCESS_CONNECTION

    def send_file(self, path: str):
        _, ext = os.path.splitext(path)
        with open(path, "rb") as f:
            self._connection.send(ext.encode())

    def __del__(self):
        if self.connection is not None:
            self.connection.shutdown(0)
            del self.connection
            self._connection = None
