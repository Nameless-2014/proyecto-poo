import wx

from views.main_frame import MainFrame


class RepairDeskApp(wx.App):

    def OnInit(self):

        frame = MainFrame()

        frame.Show()

        return True


app = RepairDeskApp()
app.MainLoop()