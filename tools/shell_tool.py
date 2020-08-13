# coding=utf-8
import os
import subprocess

from global_config.select_item import SelectItem


class ShellTool:
    env = {}

    def __init__(self):
        pass

    @staticmethod
    def init_shell_env():
        os.environ['PATH'] = SelectItem.get_adb_path() + ':' + os.environ['PATH']
        ShellTool.env.update(os.environ)

    @staticmethod
    def run(command):
        p = subprocess.Popen(command, shell=True,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=ShellTool.env)
        out, err = p.communicate()
        # out = p.stdout.read()
        # err = p.stderr.read()
        return out, err
