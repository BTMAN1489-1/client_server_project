from gui_client import ClientFrame
import wx

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = wx.App()
    f = ClientFrame(None, "Client")
    f.Show()
    app.MainLoop()
