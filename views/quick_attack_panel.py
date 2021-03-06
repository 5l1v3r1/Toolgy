# coding=utf-8
from __future__ import print_function

import os
import xml.etree.ElementTree as ET

import wx
from pubsub import pub

from global_config.select_item import SelectItem
from tools.component_tool import ComponentTool
from tools.device_tool import DeviceTool
from tools.frida_tool import FridaTool
from tools.general_tool import GeneralTool
from tools.package_manager_tool import PackageManagerTool
from tools.shell_tool import ShellTool

import sys

from tools.xposed_tool import XposedTool

reload(sys)
sys.setdefaultencoding('utf-8')


class QuickAttackPanel(wx.Panel):
    def __init__(self, parent):
        super(QuickAttackPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)

        # device operation
        self.staticboxsizer_devices = wx.StaticBoxSizer(wx.StaticBox(self, label='Device Operation'))
        self.boxsizer_devices = wx.BoxSizer(wx.HORIZONTAL)
        self.statictext_device_name = wx.StaticText(self, -1, label='Name:          ')
        self.statictext_device_os_version = wx.StaticText(self, -1, label='OS Version:          ')
        self.boxsizer_devices.Add(self.statictext_device_name, flag=wx.CENTER | wx.ALL, border=0)
        self.boxsizer_devices.AddSpacer(10)
        self.boxsizer_devices.Add(self.statictext_device_os_version, flag=wx.CENTER | wx.ALL, border=0)
        self.boxsizer_devices.AddSpacer(10)
        self.devices_list = []
        self.combobox_devices = wx.ComboBox(self, choices=self.devices_list)
        # self.combobox_devices.SetBackgroundColour(wx.WHITE)
        self.button_refresh_devices = wx.Button(self, label='Refresh Device List')
        self.boxsizer_devices.Add(self.combobox_devices, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_devices.AddSpacer(10)
        self.boxsizer_devices.Add(self.button_refresh_devices, flag=wx.EXPAND | wx.ALL, border=0)
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox_device_select, self.combobox_devices)
        self.Bind(wx.EVT_BUTTON, self.on_refresh_devices_list, self.button_refresh_devices)
        self.staticboxsizer_devices.Add(self.boxsizer_devices)

        # component operation
        self.staticboxsizer_component = wx.StaticBoxSizer(wx.StaticBox(self, label='Quick Attack'))
        self.boxsizer_component = wx.BoxSizer(wx.HORIZONTAL)
        self.button_activity = wx.Button(self, label='Start Activity')
        self.button_service = wx.Button(self, label='Start Service')
        self.button_broadcast = wx.Button(self, label='Send Broadcast')
        self.boxsizer_component.Add(self.button_activity, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_component.AddSpacer(10)
        self.boxsizer_component.Add(self.button_service, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_component.AddSpacer(10)
        self.boxsizer_component.Add(self.button_broadcast, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_component.AddSpacer(10)
        self.Bind(wx.EVT_BUTTON, self.on_start_activity, self.button_activity)
        self.Bind(wx.EVT_BUTTON, self.on_start_service, self.button_service)
        self.Bind(wx.EVT_BUTTON, self.on_send_broadcast, self.button_broadcast)
        self.staticboxsizer_component.Add(self.boxsizer_component)

        # Add all staticboxsizers to boxsizer_main
        self.boxsizer_main.Add(self.staticboxsizer_devices, flag=wx.EXPAND | wx.ALL, border=0)
        self.boxsizer_main.Add(self.staticboxsizer_component, flag=wx.EXPAND | wx.ALL, border=0)

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

        tree = ET.parse("./config.xml")
        adb_path = tree.getroot()[0].text.strip()
        SelectItem.set_adb_path(adb_path)

        ShellTool.init_shell_env()

        # refresh device list while starting Toolgy
        self.refresh_devices_list()
        # self.textctrl_hint.SetValue(str(ShellTool.env))

    def on_combobox_device_select(self, event):
        self.clear_all_textctrl()
        select_index = self.combobox_devices.GetSelection()
        if select_index == wx.NOT_FOUND:
            return
        device_name = self.combobox_devices.GetItems()[select_index].encode('utf-8')
        SelectItem.set_selected_device_name(device_name)
        device_name = DeviceTool.getprop_ro_product_name()
        device_os_version = DeviceTool.getprop_ro_build_version_release()
        self.statictext_device_name.SetLabel('Name: {}'.format(device_name[0]).strip())
        self.statictext_device_os_version.SetLabel('OS Version: {}'.format(device_os_version[0]).strip())

        pub.sendMessage('re_select_device')

    def on_start_activity(self, event):
        self.clear_all_textctrl()
        ComponentTool.start_activity(self)

    def on_start_service(self, event):
        self.clear_all_textctrl()
        ComponentTool.start_service(self)

    def on_send_broadcast(self, event):
        self.clear_all_textctrl()
        ComponentTool.send_broadcast(self)

    def on_refresh_devices_list(self, event):
        self.refresh_devices_list()

    def refresh_devices_list(self):
        self.clear_all_textctrl()
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
            device_name = DeviceTool.getprop_ro_product_name()
            device_os_version = DeviceTool.getprop_ro_build_version_release()
            self.statictext_device_name.SetLabel('Name: {}'.format(device_name[0]).strip())
            self.statictext_device_os_version.SetLabel('OS Version: {}'.format(device_os_version[0]).strip())
            pub.sendMessage('re_select_device')
        else:
            SelectItem.set_selected_device_name('')
            device_name = '          '
            device_os_version = '          '
            self.statictext_device_name.SetLabel('Name: {}'.format(device_name))
            self.statictext_device_os_version.SetLabel('OS Version: {}'.format(device_os_version))
            SelectItem.clear_all()
            pub.sendMessage('no_device')

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
