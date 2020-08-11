# coding=utf-8

class SelectItem:
    def __init__(self):
        pass

    selected_package_name = ''
    selected_device_name = ''
    list_all_packages = []
    list_all_packages_filepath = []
    list_system_packages = []
    list_system_packages_filepath = []
    list_third_part_packages = []
    list_third_part_packages_filepath = []

    @staticmethod
    def get_selected_package_name():
        return SelectItem.selected_package_name

    @staticmethod
    def set_selected_package_name(package_name):
        SelectItem.selected_package_name = package_name

    @staticmethod
    def get_selected_device_name():
        return SelectItem.selected_device_name

    @staticmethod
    def set_selected_device_name(device_name):
        SelectItem.selected_device_name = device_name.replace('\n', '')

    @staticmethod
    def get_all_packages_list():
        return SelectItem.list_all_packages

    @staticmethod
    def set_all_packages_list(all_packages):
        SelectItem.list_all_packages = all_packages

    @staticmethod
    def get_system_packages_list():
        return SelectItem.list_system_packages

    @staticmethod
    def set_system_packages_list(system_packages):
        SelectItem.list_system_packages = system_packages

    @staticmethod
    def get_third_part_packages_list():
        return SelectItem.list_third_part_packages

    @staticmethod
    def set_third_part_packages_list(third_part_packages):
        SelectItem.list_third_part_packages = third_part_packages


