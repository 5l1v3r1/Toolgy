# coding=utf-8
import wx

from tools.frida_tool import FridaTool
from tools.shell_tool import ShellTool
from tools.xposed_tool import XposedTool


class XposedPanel(wx.Panel):
    def __init__(self, parent):
        super(XposedPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)
        # self.SetBackgroundColour(wx.RED)

        # hook operation
        self.staticboxsizer_hook = wx.StaticBoxSizer(wx.StaticBox(self, label='Xposed'))
        self.boxsizer_hook = wx.BoxSizer(wx.HORIZONTAL)
        self.button_generate_xposed_basic_code = wx.Button(self, label='Xposed Basic Code')
        self.boxsizer_hook.Add(self.button_generate_xposed_basic_code, flag=wx.EXPAND | wx.ALL, border=0)
        self.staticboxsizer_hook.Add(self.boxsizer_hook)
        self.Bind(wx.EVT_BUTTON, self.on_generate_xposed_basic_script, self.button_generate_xposed_basic_code)
        self.boxsizer_main.Add(self.staticboxsizer_hook, flag=wx.EXPAND | wx.ALL, border=0)

        # function hint
        self.textctrl_hint = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textctrl_hint.SetBackgroundColour(wx.WHITE)
        self.boxsizer_main.Add(self.textctrl_hint, flag=wx.EXPAND | wx.ALL, border=5)

        # code editor
        self.boxsizer_code = wx.BoxSizer(wx.HORIZONTAL)
        self.textctrl_code = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.boxsizer_code.Add(self.textctrl_code, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)
        self.boxsizer_main.Add(self.boxsizer_code, flag=wx.EXPAND | wx.ALL, proportion=1)

        self.SetSizer(self.boxsizer_main)

    def on_generate_xposed_basic_script(self, event):
        self.clear_all_textctrl()
        XposedTool.generate_xposed_basic_code(self)

    def clear_all_textctrl(self):
        self.textctrl_hint.SetValue('')
        self.textctrl_code.SetValue('')
