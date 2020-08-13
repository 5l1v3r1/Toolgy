# coding=utf-8
import wx

from tools.frida_tool import FridaTool


class FridaPanel(wx.Panel):
    def __init__(self, parent):
        super(FridaPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)
        # self.SetBackgroundColour(wx.RED)

        # frida operation
        self.staticboxsizer_frida = wx.StaticBoxSizer(wx.StaticBox(self, label='Frida'))
        self.boxsizer_frida = wx.BoxSizer(wx.HORIZONTAL)
        self.button_generate_frida_basic_script = wx.Button(self, label='Frida Basic Script')
        self.button_generate_frida_native_script = wx.Button(self, label='Frida Native Script')
        self.boxsizer_frida.Add(self.button_generate_frida_basic_script, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_frida.AddSpacer(10)
        self.boxsizer_frida.Add(self.button_generate_frida_native_script, flag=wx.EXPAND | wx.ALL, border=0)
        self.staticboxsizer_frida.Add(self.boxsizer_frida)
        self.Bind(wx.EVT_BUTTON, self.on_generate_frida_basic_script, self.button_generate_frida_basic_script)
        self.boxsizer_main.Add(self.staticboxsizer_frida, flag=wx.EXPAND | wx.ALL, border=0)

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

    def on_generate_frida_basic_script(self, event):
        self.clear_all_textctrl()
        FridaTool.generate_frida_basic_script(self)

    def clear_all_textctrl(self):
        self.textctrl_hint.SetValue('')
        self.textctrl_code.SetValue('')
