# coding=utf-8
import wx

from global_config.select_item import SelectItem
from tools.general_tool import GeneralTool
from tools.package_manager_tool import PackageManagerTool
from tools.shell_tool import ShellTool


class DevicePanel(wx.Panel):
    def __init__(self, parent):
        super(DevicePanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)
        # self.SetBackgroundColour(wx.RED)

        # general operation
        self.staticboxsizer_operation = wx.StaticBoxSizer(wx.StaticBox(self, label='Device Operation'))
        self.boxsizer_operation = wx.BoxSizer(wx.HORIZONTAL)
        self.button_operation = wx.Button(self, label='Backup App')
        self.button_top_activity = wx.Button(self, label='Top Activity')
        self.button_device_info = wx.Button(self, label='Device Info')
        self.button_insatall_app = wx.Button(self, label='Install App')
        self.button_uninsatall_app = wx.Button(self, label='Uninstall App')
        self.boxsizer_operation.Add(self.button_operation, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_operation.AddSpacer(10)
        self.boxsizer_operation.Add(self.button_top_activity, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_operation.AddSpacer(10)
        self.boxsizer_operation.Add(self.button_device_info, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_operation.AddSpacer(10)
        self.boxsizer_operation.Add(self.button_insatall_app, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_operation.AddSpacer(10)
        self.boxsizer_operation.Add(self.button_uninsatall_app, flag=wx.EXPAND | wx.ALL, border=0)
        self.Bind(wx.EVT_BUTTON, self.on_get_top_activity, self.button_top_activity)
        self.Bind(wx.EVT_BUTTON, self.on_get_device_info, self.button_device_info)
        self.Bind(wx.EVT_BUTTON, self.on_install_app, self.button_insatall_app)
        self.Bind(wx.EVT_BUTTON, self.on_uninstall_app, self.button_uninsatall_app)
        self.staticboxsizer_operation.Add(self.boxsizer_operation)
        self.boxsizer_main.Add(self.staticboxsizer_operation, flag=wx.EXPAND | wx.ALL, border=0)

        # command param hint
        self.textctrl_hint = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textctrl_hint.SetBackgroundColour(wx.WHITE)
        self.boxsizer_main.Add(self.textctrl_hint, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)

        # command editor
        self.boxsizer_command = wx.BoxSizer(wx.HORIZONTAL)
        self.textctrl_shell = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.shell_exec_button = wx.Button(self, label="Execute")
        self.boxsizer_command.Add(self.textctrl_shell, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)
        self.boxsizer_command.Add(self.shell_exec_button, flag=wx.EXPAND | wx.ALL, border=5)
        self.boxsizer_main.Add(self.boxsizer_command, flag=wx.EXPAND | wx.ALL, proportion=1)
        self.Bind(wx.EVT_BUTTON, self.on_command_exec, self.shell_exec_button)

        # command execute output
        self.textctrl_output = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.textctrl_output.SetBackgroundColour(wx.WHITE)
        self.boxsizer_main.Add(self.textctrl_output, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)

        self.SetSizer(self.boxsizer_main)

    def on_get_top_activity(self, event):
        self.clear_all_textctrl()
        GeneralTool.get_top_activity(self)

    def on_get_device_info(self, event):
        self.clear_all_textctrl()
        shell = 'adb -s {} shell getprop'.format(SelectItem.get_selected_device_name())
        self.textctrl_shell.SetValue(shell)
        out, err = ShellTool.run(shell)
        self.textctrl_output.SetValue(out)
        self.textctrl_output.AppendText('\n')
        self.textctrl_output.AppendText(err)

    def on_install_app(self, event):
        self.clear_all_textctrl()
        PackageManagerTool.install_app(self)

    def on_uninstall_app(self, event):
        self.clear_all_textctrl()
        PackageManagerTool.uninstall_app(self)

    def on_command_exec(self, event):
        shell = self.textctrl_shell.GetValue()
        out, err = ShellTool.run(shell)
        self.textctrl_output.SetValue(out)
        self.textctrl_output.AppendText('\n')
        self.textctrl_output.AppendText(err)

    def clear_all_textctrl(self):
        self.textctrl_hint.SetValue('')
        self.textctrl_shell.SetValue('')
        self.textctrl_output.SetValue('')
