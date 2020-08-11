# Toolgy

A useful tool I use in daily analysis work. 

Feel free to open an issue, thank you guys.

## How to Run
Clone the git repo to your computer.
```
git clone https://github.com/wnagzihxa1n/Toolgy.git
```

Open python IDE and import the project, my development tool is PyCharm, it's very powerful.

## How to Use
First, your system environment needs include 'adb', most of toolgy's functions are base on `adb shell` command.

Please follow the official guide to setup.
- https://developer.android.com/studio/command-line/adb

Once you run it, you will see the window as follow.

![](resources/main_window.png)

Here are two panels:`packages_panel` and `buttons_panel`.

Connect your device to computer, click the button `Refresh App List`, the list will show all apps installed in your device.

We select one item and click `Start Activity`, toolgy shows very clear description

![](resources/start_activity.png)

You could fill the component name and add some params like `--es xxx` whatever you need.

Other buttons are same as `Start Activity`.