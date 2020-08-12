# coding=utf-8
from global_config.select_item import SelectItem


class ComponentTool:
    def __init__(self, buttons_panel):
        pass

    @staticmethod
    def start_activity(quick_attack_panel):
        quick_attack_panel.textctrl_hint.SetValue(
            '''-n package_name/.component
-a action Action
--es key stringValue String
--ez key booleanValue Boolean
--ei key intValue int
--el key longValue long
--ef key floatValue float

$ adb shell am start -n package_name/.component
$ adb shell am start -n package_name/.component -a Action
$ adb shell am start -n package_name/.component --es str_arg_key "str_arg_value"''')
        quick_attack_panel.textctrl_shell.SetValue('adb -s {} shell am start -n {}/'
                                                   .format(SelectItem.get_selected_device_name(),
                                                           SelectItem.get_selected_package_name()))

    @staticmethod
    def start_service(quick_attack_panel):
        quick_attack_panel.textctrl_hint.SetValue(
            '''-n package_name/.component
-a action Action
--es key stringValue String
--ez key booleanValue Boolean
--ei key intValue int
--el key longValue long
--ef key floatValue float

$ adb shell am startservice -n package_name/.component
$ adb shell am startservice -n package_name/.component --es str_arg_key "str_arg_value"''')

        quick_attack_panel.textctrl_shell.SetValue('adb -s {} shell am startservice -n {}/'
                                                   .format(SelectItem.get_selected_device_name(),
                                                           SelectItem.get_selected_package_name()))

    @staticmethod
    def send_broadcast(buttons_panel):
        buttons_panel.textctrl_hint.SetValue('')
        buttons_panel.textctrl_shell.SetValue(
            'adb -s {} shell am broadcast -a '.format(SelectItem.get_selected_device_name()))
