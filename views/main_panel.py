# coding=utf-8
import wx

from views.quick_attack_panel import QuickAttackPanel
from views.device_panel import DevicePanel
from views.files_panel import FilesPanel
from views.frida_panel import FridaPanel
from views.poc_panel import PocPanel
from views.xposed_panel import XposedPanel


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super(MainPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        # self.SetBackgroundColour(wx.RED)

        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)

        self.notebook = wx.Notebook(self, style=wx.NB_FIXEDWIDTH)
        self.notebook.AddPage(QuickAttackPanel(self.notebook), 'Quick Attack')
        self.notebook.AddPage(FilesPanel(self.notebook), 'File')
        self.notebook.AddPage(FridaPanel(self.notebook), 'Frida')
        self.notebook.AddPage(XposedPanel(self.notebook), 'Xposed')
        self.notebook.AddPage(DevicePanel(self.notebook), 'Device')
        self.notebook.AddPage(PocPanel(self.notebook), 'Poc')

        self.boxsizer_main.Add(self.notebook, flag=wx.EXPAND | wx.ALL, border=0, proportion=1)

        self.SetSizer(self.boxsizer_main)



