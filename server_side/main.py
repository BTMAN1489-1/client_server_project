from gui_server import ServerFrame
import wx

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = wx.App()
    f = ServerFrame(None, "Server")
    f.Show()
    app.MainLoop()
