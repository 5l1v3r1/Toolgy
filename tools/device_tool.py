# coding=utf-8
from global_config.select_item import SelectItem
from tools.shell_tool import ShellTool


class DeviceTool:
    def __init__(self):
        pass

    @staticmethod
    def getprop_ro_product_name():
        return ShellTool.run("adb -s {} shell getprop ro.product.name".format(SelectItem.get_selected_device_name()))

    @staticmethod
    def getprop_ro_build_version_release():
        return ShellTool.run(
            "adb -s {} shell getprop ro.build.version.release".format(SelectItem.get_selected_device_name()))

    @staticmethod
    def get_all_packages_with_filepath():
        return ShellTool.run("adb -s {} shell pm list packages -f".format(SelectItem.get_selected_device_name()))
