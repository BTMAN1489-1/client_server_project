import wx
import pathlib
from commands import ServerConnectCommand
import socket
import config
import threading

BUTTON_START = 4
BUTTON_CANCEL = 5
BUTTON_CONNECT = 6


class AdditionalPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        static_vbox_sizer = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Server configuration")
        main_vbox = wx.BoxSizer(wx.VERTICAL)
        main_hbox = wx.GridBagSizer(0, 3)
        add_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.rd_bt_local_host = wx.RadioButton(self, label="Local Host", style=wx.RB_GROUP)
        self.rd_bt_public_host = wx.RadioButton(self, label="Public Host")
        add_hbox.Add(self.rd_bt_local_host, flag=wx.EXPAND | wx.ALL, border=10)
        add_hbox.Add(self.rd_bt_public_host, flag=wx.EXPAND | wx.ALL, border=10)

        add_vbox = wx.BoxSizer(wx.VERTICAL)
        port_text = wx.StaticText(self, label="Port")
        self.enter_port = wx.TextCtrl(self)
        add_vbox.Add(port_text, flag=wx.EXPAND | wx.ALL ^ wx.BOTTOM ^ wx.LEFT, border=10)
        add_vbox.Add(self.enter_port, flag=wx.EXPAND | wx.ALL ^ wx.TOP ^ wx.LEFT, border=10)

        main_hbox.Add(add_hbox, pos=(0, 0), flag=wx.EXPAND)
        main_hbox.Add(add_vbox, pos=(0, 3), flag=wx.EXPAND)
        main_hbox.AddGrowableCol(3)

        self.list_ctrl = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, 'Host', width=200)
        self.list_ctrl.InsertColumn(1, 'Port', width=100)
        self.list_ctrl.InsertColumn(2, 'Connecting', width=wx.LIST_AUTOSIZE_USEHEADER)

        static_box_log = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Connections")
        static_box_log.Add(self.list_ctrl, flag=wx.EXPAND | wx.ALL, proportion=1, border=10)
        static_vbox_sizer.Add(main_hbox, flag=wx.EXPAND)
        static_vbox_sizer.Add(static_box_log, flag=wx.EXPAND | wx.ALL, proportion=1, border=10)

        main_vbox.Add(static_vbox_sizer, flag=wx.ALL | wx.EXPAND, border=20, proportion=1)
        self.SetSizer(main_vbox)
        self.Layout()


class ServerFrame(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.SetMinSize((500, 400))

        self.server_instance = None

        self.sb = self.CreateStatusBar()
        main_panel = wx.Panel(self)
        main_vbox = wx.BoxSizer(wx.VERTICAL)

        add_panel = AdditionalPanel(main_panel)
        self.list_ctrl = add_panel.list_ctrl
        self.rd1_localhost = add_panel.rd_bt_local_host
        self.rd2_publichost = add_panel.rd_bt_public_host
        self.port = add_panel.enter_port

        gr_box = wx.GridBagSizer(0, 3)
        self.button_start = wx.Button(main_panel, id=BUTTON_START, label='Start', size=(80, 28))
        button_cancel = wx.Button(main_panel, id=BUTTON_CANCEL, label='Cancel', size=(80, 28))
        button_connect = wx.Button(main_panel, id=BUTTON_CONNECT, label='Connect', size=(120, 28))
        button_connect.Disable()
        gr_box.Add(button_connect, pos=(0, 0), flag=wx.ALL | wx.EXPAND, border=10)
        gr_box.Add(self.button_start, pos=(0, 2), flag=wx.ALL, border=10)
        gr_box.Add(button_cancel, pos=(0, 3), flag=wx.ALL, border=10)
        gr_box.AddGrowableCol(1)

        main_vbox.Add(add_panel, flag=wx.EXPAND | wx.BOTTOM, proportion=1, border=30)
        main_vbox.Add(gr_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        main_panel.Bind(wx.EVT_BUTTON, self.on_button_start, id=BUTTON_START)
        self.Bind(wx.EVT_BUTTON, self.on_button_cancel, id=BUTTON_CANCEL)
        self.Bind(wx.EVT_CLOSE, self.on_close_event)
        # main_panel.Bind(wx.EVT_BUTTON, self.on_button_connect, id=BUTTON_CONNECT)
        main_panel.SetSizer(main_vbox)
        main_panel.Layout()

    def update_connect_panel(self, host, port, status):
        self.list_ctrl.Append((host, port, status))
        self.Update()

    def create_connect_dialog(self):
        with wx.MessageDialog(None,
                              "Do you really want to Download file?",
                              "Download file",
                              wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) as dial:
            res = dial.ShowModal()
            if res == wx.ID_YES:
                res = True
            else:
                res = False

        return res

    def create_choose_file_dir(self):
        pwd = str(pathlib.Path.home())
        with wx.FileDialog(self, "Save file", pwd, style=wx.FD_SAVE) as fileDialog:
            fileDialog.ShowModal()
            filename = fileDialog.GetPath()
            return filename

    def on_button_start(self, event):
        host = 'localhost'
        if self.rd2_publichost.GetValue():
            host = socket.gethostname()
        port = self.port.GetValue()
        try:
            port = int(port)
        except ValueError:
            wx.LogError("Bad server configuration")
            return

        # ServerConnectCommand(self, host=host, port=port)
        self.button_start.Disable()
        self.rd1_localhost.Disable()
        self.rd2_publichost.Disable()
        self.port.Disable()
        # ServerConnectCommand(self, host, port)
        config.server_is_run = True
        self.server_instance = threading.Thread(target=ServerConnectCommand, args=(self, host, port))
        self.server_instance.start()

    def on_close_event(self, event):
        with wx.MessageDialog(None, "Do you really want to leave?", "Exit",
                              wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) as dial:
            res = dial.ShowModal()
            if res == wx.ID_YES:
                if config.server_is_run:
                    config.server_is_run = False
                    self.server_instance.join(5)
                self.Destroy()
            else:
                event.Veto()

    def on_button_cancel(self, event):
        self.Close()

    # def on_button_connect(self, event):
    #     wx.LogMessage('erretetre')
    #     print("Press button cancel")
