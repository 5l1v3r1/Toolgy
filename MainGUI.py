# coding=utf-8
# /usr/local/bin/python2.7

import wx
from views.potat0_frame import Potat0Frame


class AndroidToolgyApp(wx.App):
    def OnInit(self):
        Potat0Frame(None, 'Android Toolgy by wnagzihxa1n').Show()
        return True


def main():
    app = AndroidToolgyApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
