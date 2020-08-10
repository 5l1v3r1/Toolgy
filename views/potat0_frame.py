# coding=utf-8
# /usr/local/bin/python2.7

import os
import wx
import wx.aui
from tools.shell_tool import ShellTool
from views.all_packages_panel import AllPackagesPanel
from views.buttons_panel import ButtonsPanel


class Potat0Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Potat0Frame, self).__init__()
        wx.Frame.__init__(self, parent, title=title, size=(1300, 800))

        self.buttons_panel = ButtonsPanel(self)
        self.all_packages_panel = AllPackagesPanel(self)

        self.auiManager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_TRANSPARENT_HINT)
        self.auiManager.AddPane(self.all_packages_panel, wx.aui.AuiPaneInfo()
                                .CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False)
                                .Gripper(False).Left().Row(1).BestSize(1000, -1).MinSize(500, -1))
        self.auiManager.AddPane(self.buttons_panel, wx.aui.AuiPaneInfo()
                                .CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False)
                                .Gripper(False).CenterPane().Position(0).BestSize(600, -1))
        self.auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 1)
        self.auiManager.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Center()

    def OnClose(self, event):
        self.auiManager.UnInit()
        del self.auiManager
        self.Destroy()
