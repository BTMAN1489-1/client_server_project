import wx
import pathlib
from commands import ClientConnectCommand
import threading

BUTTON_SEND = 1
BUTTON_CANCEL = 2
BUTTON_SERVER = 3


class LogPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour('#242121')
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.log_view = wx.StaticText(self)
        self.log_view.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Consolas'))
        self.log_view.SetForegroundColour('#f50707')

        vbox.Add(self.log_view, flag=wx.EXPAND | wx.ALL, border=5, proportion=1)
        self.SetScrollbars(20, 20, 50, 50)
        self.update("--CLIENT:INFO:Start process")

        self.SetSizer(vbox)
        self.Layout()

    def update(self, log: str):
        logs = self.log_view.GetLabel() + log + "\n"
        self.log_view.SetLabelText(logs)


class AdditionalPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        static_vbox_sizer = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Connection parameters")
        main_vbox = wx.BoxSizer(wx.VERTICAL)
        main_hbox = wx.GridBagSizer(0, 3)

        add_vbox1 = wx.BoxSizer(wx.VERTICAL)
        host_text = wx.StaticText(self, label="Host")
        self.enter_host = wx.TextCtrl(self)
        add_vbox1.Add(host_text, flag=wx.EXPAND | wx.ALL ^ wx.BOTTOM ^ wx.RIGHT, border=10)
        add_vbox1.Add(self.enter_host, flag=wx.EXPAND | wx.ALL ^ wx.TOP ^ wx.RIGHT, border=10)

        add_vbox2 = wx.BoxSizer(wx.VERTICAL)
        port_text = wx.StaticText(self, label="Port")
        self.enter_port = wx.TextCtrl(self)
        add_vbox2.Add(port_text, flag=wx.EXPAND | wx.ALL ^ wx.BOTTOM ^ wx.LEFT, border=10)
        add_vbox2.Add(self.enter_port, flag=wx.EXPAND | wx.ALL ^ wx.TOP ^ wx.LEFT, border=10)

        main_hbox.Add(add_vbox1, pos=(0, 0), span=(0, 2), flag=wx.EXPAND)
        main_hbox.Add(add_vbox2, pos=(0, 3), flag=wx.EXPAND)
        main_hbox.AddGrowableCol(0)

        self.log_panel = LogPanel(self)
        static_box_log = wx.StaticBoxSizer(parent=self, orient=wx.VERTICAL, label="Log info")
        static_box_log.Add(self.log_panel, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)
        static_vbox_sizer.Add(main_hbox, flag=wx.EXPAND)
        static_vbox_sizer.Add(static_box_log, flag=wx.EXPAND | wx.ALL, proportion=1, border=10)

        main_vbox.Add(static_vbox_sizer, flag=wx.ALL | wx.EXPAND, border=20, proportion=1)
        self.SetSizer(main_vbox)
        self.Layout()


class ClientFrame(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.SetMinSize((500, 400))
        self.client_instance = None
        self.sb = self.CreateStatusBar()
        main_panel = wx.Panel(self)
        main_vbox = wx.BoxSizer(wx.VERTICAL)

        add_panel = AdditionalPanel(main_panel)
        self.log_panel = add_panel.log_panel
        self.host = add_panel.enter_host
        self.port = add_panel.enter_port

        gr_box = wx.GridBagSizer(0, 3)
        button_send = wx.Button(main_panel, id=BUTTON_SEND, label='Send', size=(80, 28))
        button_cancel = wx.Button(main_panel, id=BUTTON_CANCEL, label='Cancel', size=(80, 28))
        button_server = wx.Button(main_panel, id=BUTTON_SERVER, label='Run server', size=(120, 28))
        button_server.Disable()
        gr_box.Add(button_server, pos=(0, 0), flag=wx.ALL | wx.EXPAND, border=10)
        gr_box.Add(button_send, pos=(0, 2), flag=wx.ALL, border=10)
        gr_box.Add(button_cancel, pos=(0, 3), flag=wx.ALL, border=10)
        gr_box.AddGrowableCol(1)

        main_vbox.Add(add_panel, flag=wx.EXPAND | wx.BOTTOM, proportion=1, border=30)
        main_vbox.Add(gr_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        main_panel.Bind(wx.EVT_BUTTON, self.on_button_send, id=BUTTON_SEND)
        self.Bind(wx.EVT_BUTTON, self.on_button_cancel, id=BUTTON_CANCEL)
        self.Bind(wx.EVT_CLOSE, self.on_close_event)
        # main_panel.Bind(wx.EVT_BUTTON, self.on_button_server, id=BUTTON_SERVER)
        main_panel.SetSizer(main_vbox)
        main_panel.Layout()

    def update_log_panel(self, new_log: str):
        self.log_panel.update(new_log)
        self.Update()

    def create_choose_file_dialog(self):
        pwd = str(pathlib.Path.home())
        with wx.FileDialog(self, "Open file", pwd, style=wx.FD_OPEN) as fileDialog:
            fileDialog.ShowModal()
            pathname = fileDialog.GetPath()
            return pathname

    def on_button_send(self, event):
        host = self.host.GetValue()
        port = self.port.GetValue()
        self.client_instance = threading.Thread(target=ClientConnectCommand, args=(self, host, port))
        self.client_instance.start()

    def on_close_event(self, event):
        with wx.MessageDialog(None, "Do you really want to leave?", "Exit",
                              wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) as dial:
            res = dial.ShowModal()
            if res == wx.ID_YES:
                if self.client_instance is not None:
                    self.client_instance.join()
                self.Destroy()
            else:
                event.Veto()

    def on_button_cancel(self, event):
        self.Close()

    # def on_button_server(self, event):
    #     wx.LogMessage('erretetre')
    #     print("Press button cancel")