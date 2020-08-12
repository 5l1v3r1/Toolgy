# coding=utf-8
import wx

from tools.frida_tool import FridaTool
from tools.poc_tool import PocTool
from tools.shell_tool import ShellTool
from tools.xposed_tool import XposedTool


class PocPanel(wx.Panel):
    def __init__(self, parent):
        super(PocPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)
        # self.SetBackgroundColour(wx.RED)

        # hook operation
        self.staticboxsizer_poc = wx.StaticBoxSizer(wx.StaticBox(self, label='Android'))
        self.boxsizer_poc = wx.BoxSizer(wx.HORIZONTAL)
        self.button_generate_intent_logic_vul_poc = wx.Button(self, label='Intent Logic Vul Poc')
        self.button_generate_intent_attack_poc = wx.Button(self, label='Intent DOS Poc')
        self.boxsizer_poc.Add(self.button_generate_intent_logic_vul_poc, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_poc.AddSpacer(10)
        self.boxsizer_poc.Add(self.button_generate_intent_attack_poc, flag=wx.EXPAND | wx.ALL, border=0)
        self.staticboxsizer_poc.Add(self.boxsizer_poc)
        self.Bind(wx.EVT_BUTTON, self.on_generate_android_intent_logic_vul_poc, self.button_generate_intent_logic_vul_poc)
        self.Bind(wx.EVT_BUTTON, self.on_generate_android_intent_dos_poc, self.button_generate_intent_attack_poc)
        self.boxsizer_main.Add(self.staticboxsizer_poc, flag=wx.EXPAND | wx.ALL, border=0)

        # poc
        self.textctrl_poc = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textctrl_poc.SetBackgroundColour(wx.WHITE)
        self.boxsizer_main.Add(self.textctrl_poc, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)

        self.SetSizer(self.boxsizer_main)

    def on_generate_android_intent_logic_vul_poc(self, event):
        PocTool.generate_android_intent_logic_vul_poc(self)

    def on_generate_android_intent_dos_poc(self, event):
        PocTool.generate_android_intent_dos_poc(self)

