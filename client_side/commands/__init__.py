import socket

from client_side import ClientSocket
from client_side.misc import StatusCode, validate_address, validate_pathname, create_log
import wx


class ClientConnectCommand:
    _conn = None
    _client = None

    def __new__(cls, gui_instance, host, port, *args, **kwargs):
        status: StatusCode = cls._connect(host, port)
        match status:
            case StatusCode.FAILED_VALIDATE_ADDR:
                _, log = create_log(status)
                gui_instance.update_log_panel(log)
                return status
            case StatusCode.SUCCESS_VALIDATE_ADDR:
                _, log = create_log(status)
                gui_instance.update_log_panel(log)

            case StatusCode.SUCCESS_CONNECTION:
                _, log = create_log(status, host=host, port=port)
                gui_instance.update_log_panel(log)

            case StatusCode.FAILED_CONNECTION:
                message, log = create_log(status, host=host, port=port)
                gui_instance.update_log_panel(log)
                wx.LogError(message)
                return status

        pathname = gui_instance.create_choose_file_dialog()
        status = validate_pathname(pathname)
        match status:
            case StatusCode.SUCCESS_OPEN_FILE:
                _, log = create_log(status, pathname=pathname)
                gui_instance.update_log_panel(log)

            case StatusCode.FAILED_OPEN_FILE:
                if pathname != '':
                    message, log = create_log(status, pathname=pathname)
                    gui_instance.update_log_panel(log)
                    wx.LogError(message)
                cls.shutdown_connection()
                return status
        try:
            with open(pathname, "rb") as f:
                cls._client.connection.sendfile(f)
        except socket.error:
            message, log = create_log(StatusCode.FAILED_UPLOAD_FILE, host=host, port=port, pathname=pathname)
            gui_instance.update_log_panel(log)
            wx.LogError(message)
        else:
            message, log = create_log(StatusCode.SUCCESS_UPLOAD_FILE, host=host, port=port, pathname=pathname)
            gui_instance.update_log_panel(log)
            wx.LogMessage(message)
        finally:
            cls.shutdown_connection()

    @classmethod
    def _connect(cls, host, port):
        status = validate_address(host, port)
        if status == StatusCode.FAILED_VALIDATE_ADDR:
            return status

        cls._client = ClientSocket(host, int(port))
        status = cls._client.create_connection()

        return status


    @classmethod
    def shutdown_connection(cls):
        del cls._client

