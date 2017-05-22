# midiscriptor
Control your Linux system with MIDI devices


## Requirements

* A Linux system (may work on other systems if you do the necessary)
* A MIDI-USB device (works also with a (second) USB keboard)
* [Python 3](https://www.python.org/downloads)
* [libusb](http://libusb.info/) or [OpenUSB](https://sourceforge.net/projects/openusb/)
* [PyUSB](https://github.com/walac/pyusb#installing-pyusb-on-gnulinux-systems): `sudo pip3 install pyusb`

Only if you want to use the keyboard mode:  
* [PyUserInput](https://github.com/PyUserInput/PyUserInput): `sudo pip3 install pyuserinput`
* [pyperclip](https://github.com/asweigart/pyperclip): `sudo pip3 install pyperclip`
* [xsel](https://github.com/kfish/xsel): `sudo apt-get install xsel`

Only if you want to run the `midipaint.py` and `background.py` examples:  
* [pyGame](http://www.pygame.org/download.shtml): `sudo pip3 install pygame`

## User guide

3 modes:

* output: midiscriptor produces standard outputs, which can be used using pipes.
* command: midiscriptor subprocesses user defined command.
* keyboard: midiscriptor acts like a computer keyboard: user defined text is written where the focus is.
