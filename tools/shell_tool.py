# coding=utf-8

import subprocess


class ShellTool:
    def __init__(self):
        pass

    @staticmethod
    def run(command):
        p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        out, err = p.communicate()
        return out, err
