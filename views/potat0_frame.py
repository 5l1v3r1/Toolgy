# coding=utf-8
# /usr/local/bin/python2.7
import os

import wx
import wx.aui
import xml.etree.ElementTree as ET

from global_config.select_item import SelectItem
from tools.shell_tool import ShellTool
from views.all_packages_panel import AllPackagesPanel
from views.main_panel import MainPanel


class Potat0Frame(wx.Frame):
    def __init__(self, parent, title):
        super(Potat0Frame, self).__init__()
        wx.Frame.__init__(self, parent, title=title, size=(1300, 800))

        self.main_panel = MainPanel(self)
        self.all_packages_panel = AllPackagesPanel(self)

        self.auiManager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_TRANSPARENT_HINT)
        self.auiManager.AddPane(self.all_packages_panel, wx.aui.AuiPaneInfo()
                                .CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False)
                                .Gripper(False).Left().Row(1).BestSize(1000, -1).MinSize(500, -1))
        self.auiManager.AddPane(self.main_panel, wx.aui.AuiPaneInfo()
                                .CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False)
                                .Gripper(False).CenterPane().Position(0).BestSize(600, -1))
        self.auiManager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 1)
        self.auiManager.Update()

        self.menubar = wx.MenuBar()
        menu_config = wx.Menu()
        menu_item_adb_path = menu_config.Append(-1, "&Adb Path", "Config your adb path")
        self.menubar.Append(menu_config, "&Config")
        self.Bind(wx.EVT_MENU, self.on_menu_adb_path, menu_item_adb_path)

        menu_about = wx.Menu()
        menu_item_author = menu_about.Append(-1, "&Author", "Know about the author")
        self.menubar.Append(menu_about, "&About")
        self.Bind(wx.EVT_MENU, self.on_menu_author, menu_item_author)

        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Center()

    def on_close(self, event):
        self.auiManager.UnInit()
        del self.auiManager
        self.Destroy()

    def on_menu_adb_path(self, event):
        dialog = wx.TextEntryDialog(self,
                                    'Example: "yourpath/android-sdk-macosx/platform-tools/"',
                                    'Set Your Adb Path',
                                    '')
        if dialog.ShowModal() == wx.ID_OK:
            new_adb_path = dialog.GetValue()
            tree = ET.parse("./config.xml")
            root = tree.getroot()
            # "/Users/wnagzihxa1n/Library/Android/android-sdk-macosx/platform-tools"
            root[0].text = new_adb_path
            tree.write("./config.xml")
            SelectItem.set_adb_path(new_adb_path)
            ShellTool.init_shell_env()

    def on_menu_author(self, event):
        dialog = wx.MessageDialog(self, "Author : wnagzihxa1n\nEmail : wnagzihxa1n@gmail.com", "Android Toolgy", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
