![Affiche](https://image.noelshack.com/fichiers/2017/48/1/1511800550-midiscriptor-affiche-1.png)

# midiscriptor
Control your Linux system with MIDI-USB controllers


## Requirements

* A Linux system (may work on other systems if you do the necessary)
* A MIDI-USB device (works also with a (second) USB keboard)
* [Python 3](https://www.python.org/downloads)
* [libusb](http://libusb.info/) or [OpenUSB](https://sourceforge.net/projects/openusb/) (Normally already present in Linux distributions)
* [PyUSB](https://github.com/walac/pyusb#installing-pyusb-on-gnulinux-systems): `sudo pip3 install pyusb`

Only if you want to use the keyboard mode:  
* [PyUserInput](https://github.com/PyUserInput/PyUserInput): `sudo pip3 install pyuserinput`
* [pyperclip](https://github.com/asweigart/pyperclip): `sudo pip3 install pyperclip`
* [xsel](https://github.com/kfish/xsel): `sudo apt-get install xsel`

Only if you want to run the `midipaint.py` and `background.py` examples:  
* [pyGame](http://www.pygame.org/download.shtml): `sudo pip3 install pygame`

## Usage

First you will have to create a configuration file to let your OS connect to your USB device.
For that run the configuration script : 

```
sudo python3 configure_device.py
```

This will create a JSON formatted configuration file. You can use it as a parameter of the configuration script to customize it : `sudo python3 configure_device.py config.json` or you can edit it as text.

Then you can use your configuration to run midiscriptor :

```
sudo python3 run.py config.json
```

3 modes:

* output: midiscriptor produces standard outputs, which can be used using pipes.
* command: midiscriptor subprocesses user defined command.
* keyboard: midiscriptor acts like a computer keyboard: user defined text is written where the focus is.

In command and keyboard mode, you will need to configure actions in your configuration file. Actions are commands to run in command mode and texts to paste in keyboard mode.

In command mode, you can use the syntax `{{a:b}}` anywhere in the action to let know midiscriptor that this needs to be replaced by a value between a and b. The value is the velocity of the key touched or the rotation of the knob turned.

No actions required in output mode, this mode will just outputs the data from your device formatted as `a;b;c:d`, where :
- `a` represents the type of input, for example: 9 for "key pressed", 8 for "key release", 11 for "knob turned"
- `c` represents the ID of the input touched
- `d` is the value of the input (velocity of key or rotation of knob)

Developers can use this formatted data in a custom program using pipes, like :

```
sudo python3 run.py output_config.json | python3 some_program.py
```

Examples of program interpreting this data are available in the `examples/output_mode` directory.
