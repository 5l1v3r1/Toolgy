# coding=utf-8
import os

import wx

from global_config.select_item import SelectItem


class PackageManagerTool:
    def __init__(self):
        self.__init__()

    @staticmethod
    def get_all_apps(self):
        pass

    @staticmethod
    def install_app(buttons_panel):
        dir_name = ''
        dialog = wx.FileDialog(buttons_panel, 'Choose a apk file', dir_name, "", "*.*", wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            file_name = dialog.GetFilename()
            dir_name = dialog.GetDirectory()
            file_path = os.path.join(dir_name, file_name)
            buttons_panel.textctrl_shell.SetValue('adb install {}'.format(file_path.replace(' ', '\ ')))

    @staticmethod
    def uninstall_app(buttons_panel):
        device_name = SelectItem.get_selected_device_name()
        uninstall_app_package = SelectItem.get_selected_package_name()
        shell = 'adb -s {} uninstall {}'.format(device_name, uninstall_app_package)
        buttons_panel.textctrl_shell.SetValue(shell)
