# coding=utf-8
import wx


class FilesPanel(wx.Panel):
    def __init__(self, parent):
        super(FilesPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)
        # self.SetBackgroundColour(wx.RED)

        self.SetSizer(self.boxsizer_main)

