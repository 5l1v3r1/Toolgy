# coding=utf-8
from global_config.select_item import SelectItem


class ComponentTool:
    def __init__(self, buttons_panel):
        pass

    @staticmethod
    def start_activity(buttons_panel):
        print("启动Activity")
        buttons_panel.textctrl_hint.SetValue('''-n 包名/组件名 指定组件启动
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
        buttons_panel.textctrl_shell.SetValue('adb -s {} shell am start -n {}/'
                                              .format(SelectItem.get_selected_device_name(),
                                                      SelectItem.get_selected_package_name()))

    @staticmethod
    def start_service(buttons_panel):
        print("启动Service")
        buttons_panel.textctrl_hint.SetValue('''-n 包名/组件名 指定组件启动
-a action 指定启动Action
--es key stringValue String类型参数
--ez key booleanValue Boolean类型参数
--ei key intValue int整型参数
--el key longValue long长整型参数
--ef key floatValue float浮点数参数

不带参数启动：adb shell am startservice -n 包名/组件名
带参数启动：adb shell am startservice -n 包名/组件名 --es str_arg_key "str_arg_value"
        ''')
        buttons_panel.textctrl_shell.SetValue('adb -s {} shell am startservice -n {}/'
                                              .format(SelectItem.get_selected_device_name(),
                                                      SelectItem.get_selected_package_name()))

    @staticmethod
    def send_broadcast(buttons_panel):
        print("发送Broadcast")
        buttons_panel.textctrl_hint.SetValue('')
        buttons_panel.textctrl_shell.SetValue(
            'adb -s {} shell am broadcast -a '.format(SelectItem.get_selected_device_name()))
