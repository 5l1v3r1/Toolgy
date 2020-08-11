# coding=utf-8
from __future__ import print_function

import wx
from pubsub import pub

from global_config.select_item import SelectItem
from tools.shell_tool import ShellTool

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class ButtonsPanel(wx.Panel):
    def __init__(self, parent):
        super(ButtonsPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        # self.SetBackgroundColour(wx.WHITE)
        self.boxsizer_main = wx.BoxSizer(wx.VERTICAL)

        # 设备操作
        self.boxsizer_devices = wx.BoxSizer(wx.HORIZONTAL)
        self.devices_list = []
        self.combobox_devices = wx.ComboBox(self, choices=self.devices_list)
        self.button_refresh_devices = wx.Button(self, label="刷新设备列表")
        self.boxsizer_devices.Add(self.combobox_devices, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_devices.Add(self.button_refresh_devices, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_COMBOBOX, self.on_combobox_device_select, self.combobox_devices)
        self.Bind(wx.EVT_BUTTON, self.on_refresh_devices_list, self.button_refresh_devices)

        # 启动四大组件
        self.boxsizer_component = wx.BoxSizer(wx.HORIZONTAL)
        self.button_activity = wx.Button(self, label="启动Activity")
        self.button_service = wx.Button(self, label="启动Service")
        self.button_broadcast = wx.Button(self, label="发送Broadcast")
        self.boxsizer_component.Add(self.button_activity, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_component.Add(self.button_service, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_component.Add(self.button_broadcast, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_BUTTON, self.on_start_activity, self.button_activity)
        self.Bind(wx.EVT_BUTTON, self.on_start_service, self.button_service)
        self.Bind(wx.EVT_BUTTON, self.on_send_broadcast, self.button_broadcast)

        # 常规操作
        self.boxsizer_operation = wx.BoxSizer(wx.HORIZONTAL)
        self.button_operation = wx.Button(self, label="备份应用")
        self.button_top_activity = wx.Button(self, label="顶部Activity")
        self.button_device_info = wx.Button(self, label="手机信息")
        self.boxsizer_operation.Add(self.button_operation, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_operation.Add(self.button_top_activity, flag=wx.EXPAND | wx.ALL, border=10)
        self.boxsizer_operation.Add(self.button_device_info, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_BUTTON, self.on_get_top_activity, self.button_top_activity)
        self.Bind(wx.EVT_BUTTON, self.on_get_device_info, self.button_device_info)

        self.boxsizer_main.Add(self.boxsizer_devices)
        self.boxsizer_main.Add(self.boxsizer_component)
        self.boxsizer_main.Add(self.boxsizer_operation)

        # self.package_name_version = wx.StaticText(self)
        # self.package_name_version.SetLabel("MD5 : \nVersion : ")
        # self.main_boxsizer.Add(self.package_name_version, flag=wx.LEFT | wx.RIGHT | wx.ALL, border=10)
        # self.main_boxsizer.AddSpacer(10)

        # self.detail = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.EXPAND)
        # self.detail.SetFont(wx.Font(12, wx.TELETYPE, wx.NORMAL, wx.NORMAL))
        # self.detail.SetBackgroundColour("#FFEC8B")
        # self.main_boxsizer.Add(self.detail, flag=wx.ALL | wx.EXPAND, border=0, proportion=1)

        # 命令参数提示窗口
        self.textctrl_hint = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textctrl_hint.SetBackgroundColour(wx.WHITE)
        self.boxsizer_main.Add(self.textctrl_hint, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)

        # 命令行窗口
        self.boxsizer_command = wx.BoxSizer(wx.HORIZONTAL)
        self.textctrl_shell = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.shell_exec_button = wx.Button(self, label="执行")
        self.boxsizer_command.Add(self.textctrl_shell, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)
        self.boxsizer_command.Add(self.shell_exec_button, flag=wx.EXPAND | wx.ALL, border=5)
        self.boxsizer_main.Add(self.boxsizer_command, flag=wx.EXPAND | wx.ALL, proportion=1)
        self.Bind(wx.EVT_BUTTON, self.on_command_exec, self.shell_exec_button)

        # 命令执行输出
        self.textctrl_output = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.textctrl_output.SetBackgroundColour(wx.WHITE)
        self.boxsizer_main.Add(self.textctrl_output, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)

        # 状态栏，没作用，就是好看
        self.statusbar = wx.StatusBar(self)
        self.boxsizer_main.Add(self.statusbar)

        self.SetSizer(self.boxsizer_main)

        # 应用启动时刷新设备列表
        self.refresh_devices_list()

    def on_combobox_device_select(self, event):
        select_index = self.combobox_devices.GetSelection()
        if select_index == wx.NOT_FOUND:
            return
        device_name = self.combobox_devices.GetItems()[select_index].encode('utf-8')
        SelectItem.set_selected_device_name(device_name)

        pub.sendMessage('re_select_device')

    def on_start_activity(self, event):
        print("启动Activity")
        self.textctrl_hint.SetValue('''-n 包名/组件名 指定组件启动
-a action 指定启动Action
--es key stringValue String类型参数
--ez key booleanValue Boolean类型参数
--ei key intValue int整型参数
--el key longValue long长整型参数
--ef key floatValue float浮点数参数

不带参数启动：adb shell am start -n 包名/组件名
指定Action启动：adb shell am start -n 包名/组件名 -a Action
带参数启动：adb shell am start -n 包名/组件名 --es str_arg_key "str_arg_value"
        ''')
        self.textctrl_shell.SetValue('adb -s {} shell am start -n {}/'
                                     .format(SelectItem.get_selected_device_name(),
                                             SelectItem.get_selected_package_name()))

    def on_start_service(self, event):
        print("启动Service")
        self.textctrl_hint.SetValue('''-n 包名/组件名 指定组件启动
-a action 指定启动Action
--es key stringValue String类型参数
--ez key booleanValue Boolean类型参数
--ei key intValue int整型参数
--el key longValue long长整型参数
--ef key floatValue float浮点数参数

不带参数启动：adb shell am startservice -n 包名/组件名
带参数启动：adb shell am startservice -n 包名/组件名 --es str_arg_key "str_arg_value"
        ''')
        self.textctrl_shell.SetValue('adb -s {} shell am startservice -n {}/'
                                     .format(SelectItem.get_selected_device_name(),
                                             SelectItem.get_selected_package_name()))

    def on_send_broadcast(self, event):
        print("发送Broadcast")
        self.textctrl_hint.SetValue('')
        self.textctrl_shell.SetValue('adb -s {} shell am broadcast -a '.format(SelectItem.get_selected_device_name()))

    def on_refresh_devices_list(self, event):
        print("刷新设备列表")
        self.textctrl_hint.SetValue('')
        self.refresh_devices_list()

    def refresh_devices_list(self):
        print("refresh_devices_list()")
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
            print("选中了 ==> " + SelectItem.get_selected_device_name())

    def on_get_top_activity(self, event):
        self.textctrl_hint.SetValue('')
        device_build_version = ShellTool.run("adb -s {} shell getprop ro.build.version.release"
                                             .format(SelectItem.get_selected_device_name()))
        shell = ''
        if device_build_version[0].startswith("7"):
            shell = 'adb -s {} shell dumpsys activity | grep "mFocusedActivity"'\
                .format(SelectItem.get_selected_device_name())
        elif device_build_version[0].startswith("8"):
            shell = 'adb -s {} shell dumpsys activity activities | grep "mResumedActivity"'\
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
