# coding=utf-8
import os

import wx


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
    def uninstall_app(buttons_panel, package_name):
        pass
