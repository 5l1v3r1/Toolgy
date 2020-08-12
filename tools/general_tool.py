# coding=utf-8
from global_config.select_item import SelectItem
from tools.device_tool import DeviceTool
from tools.shell_tool import ShellTool


class GeneralTool:
    def __init__(self):
        pass

    @staticmethod
    def get_top_activity(device_panel):
        device_build_version = DeviceTool.getprop_ro_build_version_release()
        shell = ''
        if device_build_version[0].startswith("7"):
            shell = 'adb -s {} shell dumpsys activity | grep "mFocusedActivity"' \
                .format(SelectItem.get_selected_device_name())
        elif device_build_version[0].startswith("8"):
            shell = 'adb -s {} shell dumpsys activity activities | grep "mResumedActivity"' \
                .format(SelectItem.get_selected_device_name())
        device_panel.textctrl_shell.SetValue(shell)
        out, err = ShellTool.run(shell)
        device_panel.textctrl_output.SetValue(out)
        device_panel.textctrl_output.AppendText('\n')
        device_panel.textctrl_output.AppendText(err)
