# coding=utf-8

class FridaTool:
    def __init__(self):
        pass

    @staticmethod
    def generate_frida_basic_script(frida_panel):
        frida_panel.textctrl_code.SetValue('''import frida, sys

package_name = ''

def on_message(message, data):
    if message['type'] == 'send':
        print("{}".format(message['payload']))
    else:
        print(message)

    jscode = \'\'\'
        Java.perform(function () {
        var class_xxx = Java.use('');
        class_xxx.function_yyy.implementation = function (param_1, param_2) {
                var result = this.function_yyy(param_1, param_2);
                return result;
            };
        });
    \'\'\'

process = frida.get_usb_device().attach(package_name)
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()''')
