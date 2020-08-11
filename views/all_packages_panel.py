# coding=utf-8
from __future__ import print_function

from pubsub import pub
import wx

from global_config.select_item import SelectItem
from tools.device_tool import DeviceTool
from tools.shell_tool import ShellTool


class AllPackagesPanel(wx.Panel):
    def __init__(self, parent):
        super(AllPackagesPanel, self).__init__(parent=parent, style=wx.BORDER_NONE)
        # self.SetBackgroundColour(wx.GREEN)
        self.boxSizer = wx.BoxSizer(wx.VERTICAL)
        self.listCtrl_packages = []
        self.listCtrl_filepaths = []

        # 过滤器
        self.filter_boxsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.checkbox_all_packages = wx.CheckBox(self, label='All App')
        self.checkbox_system_packages = wx.CheckBox(self, label='System App')
        self.checkbox_third_part_packages = wx.CheckBox(self, label='Third Part App')
        self.refresh_button = wx.Button(self, label='Refresh App List')

        self.filter_boxsizer.Add(self.checkbox_all_packages, flag=wx.EXPAND | wx.ALL, border=10)
        self.filter_boxsizer.Add(self.checkbox_system_packages, flag=wx.EXPAND | wx.ALL, border=10)
        self.filter_boxsizer.Add(self.checkbox_third_part_packages, flag=wx.EXPAND | wx.ALL, border=10)
        self.filter_boxsizer.Add(self.refresh_button, flag=wx.EXPAND | wx.ALL, border=10)
        self.Bind(wx.EVT_CHECKBOX, self.on_select_all_packages, self.checkbox_all_packages)
        self.Bind(wx.EVT_CHECKBOX, self.on_select_system_packages, self.checkbox_system_packages)
        self.Bind(wx.EVT_CHECKBOX, self.on_select_third_packages, self.checkbox_third_part_packages)
        self.Bind(wx.EVT_BUTTON, self.on_refresh_packages_info, self.refresh_button)
        self.boxSizer.Add(self.filter_boxsizer)

        # ListCtrl版本
        self.listCtrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.listCtrl.SetBackgroundColour('#90EE90')
        self.listCtrl.InsertColumn(0, 'Num', wx.LIST_FORMAT_CENTER, width=50)
        self.listCtrl.InsertColumn(1, 'Package Name', wx.LIST_FORMAT_LEFT, width=300)
        self.listCtrl.InsertColumn(2, 'APK Path', wx.LIST_FORMAT_LEFT, width=500)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_list_box_item_click, self.listCtrl)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_list_box_item_double_click, self.listCtrl)
        self.boxSizer.Add(self.listCtrl, flag=wx.EXPAND, proportion=1)

        self.SetSizer(self.boxSizer)

        if SelectItem.get_selected_device_name() != '':
            self.init_packages_list()
            self.checkbox_third_part_packages.SetValue(True)
            self.refresh_listctrl(SelectItem.get_third_part_packages_list())

        pub.subscribe(self.re_select_device, 're_select_device')
        pub.subscribe(self.no_device, 'no_device')

    def no_device(self):
        self.checkbox_all_packages.SetValue(False)
        self.checkbox_system_packages.SetValue(False)
        self.checkbox_third_part_packages.SetValue(False)
        self.listCtrl.DeleteAllItems()

    def re_select_device(self):
        self.init_packages_list()
        self.checkbox_third_part_packages.SetValue(True)
        self.refresh_listctrl(SelectItem.get_third_part_packages_list())

    def on_refresh_packages_info(self, event):
        self.init_packages_list()
        self.checkbox_all_packages.SetValue(False)
        self.checkbox_system_packages.SetValue(False)
        self.checkbox_third_part_packages.SetValue(True)
        self.refresh_listctrl(SelectItem.get_third_part_packages_list())

    def on_list_box_item_click(self, event):
        print(event.GetIndex(), self.listCtrl_packages[event.GetIndex()])
        SelectItem.set_selected_package_name(self.listCtrl_packages[event.GetIndex()])

    def on_list_box_item_double_click(self, event):
        print(event.GetIndex(), self.listCtrl_packages[event.GetIndex()])

    def init_packages_list(self):
        out, err = DeviceTool.get_all_packages_with_filepath()
        packages = out.split('\n')
        SelectItem.set_all_packages_list(packages)
        temp_system_packages = []
        temp_third_part_packages = []
        for package in packages:
            if 'package:/system/' in package or 'package:/vendor/' in package or 'package:/product/overlay' in package:
                temp_system_packages.append(package.replace('==/base.apk', ''))
            else:
                temp_third_part_packages.append(package.replace('==/base.apk', ''))

        SelectItem.set_system_packages_list(temp_system_packages)
        SelectItem.set_third_part_packages_list(temp_third_part_packages)

    def refresh_listctrl(self, packages):
        self.listCtrl.DeleteAllItems()

        i = 0
        for package in packages:
            if len(package.strip()) == 0:
                continue
            i = i + 1
            index = self.listCtrl.InsertItem(self.listCtrl.GetItemCount(), str(i))
            apk_filepath = package.split('=')[0].replace('package:', '')
            package_name = package.split('=')[1]
            self.listCtrl.SetItem(index, 1, package_name)
            self.listCtrl.SetItem(index, 2, apk_filepath)
            self.listCtrl.SetItemFont(self.listCtrl.GetItemCount() - 1, wx.Font(wx.FontInfo(12)))
            self.listCtrl.SetItemBackgroundColour(self.listCtrl.GetItemCount() - 1, '#FFF68F')
            self.listCtrl_packages.append(package_name)

    def on_select_all_packages(self, event):
        self.checkbox_all_packages.SetValue(True)
        self.checkbox_system_packages.SetValue(False)
        self.checkbox_third_part_packages.SetValue(False)

        if len(SelectItem.list_all_packages) == 0:
            self.init_packages_list()
        self.refresh_listctrl(SelectItem.get_all_packages_list())

    def on_select_system_packages(self, event):
        self.checkbox_all_packages.SetValue(False)
        self.checkbox_system_packages.SetValue(True)
        self.checkbox_third_part_packages.SetValue(False)

        if len(SelectItem.list_all_packages) == 0:
            self.init_packages_list()
        self.refresh_listctrl(SelectItem.get_system_packages_list())

    def on_select_third_packages(self, event):
        self.checkbox_all_packages.SetValue(False)
        self.checkbox_system_packages.SetValue(False)
        self.checkbox_third_part_packages.SetValue(True)

        if len(SelectItem.list_all_packages) == 0:
            self.init_packages_list()
        self.refresh_listctrl(SelectItem.get_third_part_packages_list())
