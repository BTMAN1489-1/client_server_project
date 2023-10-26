import socket
from server_side import init_server, selector, KindConnect
import wx
import config


class ServerConnectCommand:
    _gui_instance = None

    def __new__(cls, gui_instance, host, port, *args, **kwargs):
        cls._gui_instance = gui_instance
        try:
            init_server(host, port)
        except socket.error:
            wx.LogError("Failed running server")
            return

        while True:
            print(config.server_is_run)
            if config.server_is_run:
                events = selector.select()
                for key, _ in events:
                    print("key")
                    callback = key.data[1]
                    if key.data[0] == KindConnect.NEW_CONNECT:
                        client_socket, addr = key.fileobj.accept()
                        status = cls._gui_instance.create_connect_dialog()
                        if status:
                            client_socket.send('OK'.encode('UTF-8'))
                            cls._gui_instance.update_connect_panel(host, port, "connecting")
                            callback(client_socket)
                        else:
                            client_socket.send('WRONG'.encode('UTF-8'))
                            client_socket.close()

                    if key.data[0] == KindConnect.RECV_DATA:
                        filename = cls._gui_instance.create_choose_file_dir()
                        if filename != '':
                            callback(key.fileobj, filename)
                        else:
                            key.fileobj.close()
                            return
            else:
                return


