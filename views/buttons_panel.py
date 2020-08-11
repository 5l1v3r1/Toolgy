# coding=utf-8
from __future__ import print_function

import wx
from pubsub import pub

from global_config.select_item import SelectItem
from tools.component_tool import ComponentTool
from tools.shell_tool import ShellTool

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ButtonsPanel(wx.Panel):
    def __init__(self, parent):
        super(ButtonsPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)

        # device info
        self.boxsizer_device_info = wx.BoxSizer(wx.HORIZONTAL)
        self.statictext_device_name = wx.StaticText(self, label='Name:')
        self.statictext_device_os_version = wx.StaticText(self, label='OS Version:')
        self.boxsizer_device_info.Add(self.statictext_device_name, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_device_info.Add(self.statictext_device_os_version, flag=wx.EXPAND | wx.ALL, border=10)

        # device operation
        self.boxsizer_devices = wx.BoxSizer(wx.HORIZONTAL)
        self.devices_list = []
        self.combobox_devices = wx.ComboBox(self, choices=self.devices_list)
        self.button_refresh_devices = wx.Button(self, label="Refresh Device List")
        self.boxsizer_devices.Add(self.combobox_devices, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_devices.Add(self.button_refresh_devices, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox_device_select, self.combobox_devices)
        self.Bind(wx.EVT_BUTTON, self.on_refresh_devices_list, self.button_refresh_devices)

        # component operation
        self.boxsizer_component = wx.BoxSizer(wx.HORIZONTAL)
        self.button_activity = wx.Button(self, label="Start Activity")
        self.button_service = wx.Button(self, label="Start Service")
        self.button_broadcast = wx.Button(self, label="Send Broadcast")
        self.boxsizer_component.Add(self.button_activity, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_component.Add(self.button_service, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_component.Add(self.button_broadcast, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_BUTTON, self.on_start_activity, self.button_activity)
        self.Bind(wx.EVT_BUTTON, self.on_start_service, self.button_service)
        self.Bind(wx.EVT_BUTTON, self.on_send_broadcast, self.button_broadcast)

        # general operation
        self.boxsizer_operation = wx.BoxSizer(wx.HORIZONTAL)
        self.button_operation = wx.Button(self, label="Backup App")
        self.button_top_activity = wx.Button(self, label="Top Activity")
        self.button_device_info = wx.Button(self, label="Device Info")
        self.boxsizer_operation.Add(self.button_operation, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_operation.Add(self.button_top_activity, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_operation.Add(self.button_device_info, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_BUTTON, self.on_get_top_activity, self.button_top_activity)
        self.Bind(wx.EVT_BUTTON, self.on_get_device_info, self.button_device_info)

        self.boxsizer_main.Add(self.boxsizer_device_info)
        self.boxsizer_main.Add(self.boxsizer_devices)
        self.boxsizer_main.Add(self.boxsizer_component)
        self.boxsizer_main.Add(self.boxsizer_operation)

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

        # StatusBar, useless, just add for fun
        self.statusbar = wx.StatusBar(self)
        self.boxsizer_main.Add(self.statusbar)

        self.SetSizer(self.boxsizer_main)

        # refresh device list while starting Toolgy
        self.refresh_devices_list()

    def on_combobox_device_select(self, event):
        select_index = self.combobox_devices.GetSelection()
        if select_index == wx.NOT_FOUND:
            return
        device_name = self.combobox_devices.GetItems()[select_index].encode('utf-8')
        SelectItem.set_selected_device_name(device_name)
        device_os_version = ShellTool.run("adb -s {} shell getprop ro.product.name"
                                          .format(SelectItem.get_selected_device_name()))
        device_build_version = ShellTool.run("adb -s {} shell getprop ro.build.version.release"
                                             .format(SelectItem.get_selected_device_name()))

        self.statictext_device_name.SetLabel('Name: {}'.format(device_os_version[0]).strip())
        self.statictext_device_os_version.SetLabel('OS Version: {}'.format(device_build_version[0]).strip())

        pub.sendMessage('re_select_device')

    def on_start_activity(self, event):
        ComponentTool.start_activity(self)

    def on_start_service(self, event):
        ComponentTool.start_service(self)

    def on_send_broadcast(self, event):
        ComponentTool.send_broadcast(self)

    def on_refresh_devices_list(self, event):
        self.textctrl_hint.SetValue('')
        self.refresh_devices_list()

    def refresh_devices_list(self):
        self.textctrl_hint.SetValue('')
        out, err = ShellTool.run("adb devices")
        devices = out.split('\n')
        self.devices_list = []
        for device in devices:
            if len(device) > 0 and '\tdevice' in device:
                self.devices_list.append(device.replace('\tdevice', ''))
        self.combobox_devices.SetItems(self.devices_list)
        if len(self.devices_list) > 0:
            self.combobox_devices.SetValue(self.devices_list[0])
            SelectItem.set_selected_device_name(self.devices_list[0])
            device_os_version = ShellTool.run("adb -s {} shell getprop ro.product.name"
                                              .format(SelectItem.get_selected_device_name()))
            device_build_version = ShellTool.run("adb -s {} shell getprop ro.build.version.release"
                                                 .format(SelectItem.get_selected_device_name()))
            self.statictext_device_name.SetLabel('Name: {}'.format(device_os_version[0]).strip())
            self.statictext_device_os_version.SetLabel('OS Version: {}'.format(device_build_version[0]).strip())

    def on_get_top_activity(self, event):
        self.textctrl_hint.SetValue('')
        device_build_version = ShellTool.run("adb -s {} shell getprop ro.build.version.release"
                                             .format(SelectItem.get_selected_device_name()))
        shell = ''
        if device_build_version[0].startswith("7"):
            shell = 'adb -s {} shell dumpsys activity | grep "mFocusedActivity"' \
                .format(SelectItem.get_selected_device_name())
        elif device_build_version[0].startswith("8"):
            shell = 'adb -s {} shell dumpsys activity activities | grep "mResumedActivity"' \
                .format(SelectItem.get_selected_device_name())
        self.textctrl_shell.SetValue(shell)
        out, err = ShellTool.run(shell)
        self.textctrl_output.SetValue(out)
        self.textctrl_output.AppendText('\n')
        self.textctrl_output.AppendText(err)

    def on_get_device_info(self, event):
        self.textctrl_hint.SetValue('')
        shell = 'adb -s {} shell getprop'.format(SelectItem.get_selected_device_name())
        self.textctrl_shell.SetValue(shell)
        out, err = ShellTool.run(shell)
        self.textctrl_output.SetValue(out)
        self.textctrl_output.AppendText('\n')
        self.textctrl_output.AppendText(err)

    def on_command_exec(self, event):
        shell = self.textctrl_shell.GetValue()
        out, err = ShellTool.run(shell)
        self.textctrl_output.SetValue(out)
        self.textctrl_output.AppendText('\n')
        self.textctrl_output.AppendText(err)
