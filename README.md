# midiscriptor
Control your Linux system with MIDI devices


## Requirements

* A Linux system
* A MIDI-USB device (tested on Akai LPD8)
* Python 3 `python3 -V` 
* PyUSB `sudo pip3 install pyusb`

Only if you want to use the keyboard mode:  
* PyUserInput `sudo pip3 install pyuserinput`
* pyperclip `sudo pip3 install pyperclip`
* xsel `sudo apt-get install xsel`

Only if you want to run the midipaint example:  
* pyGame `sudo pip3 install pygame`

## User guide

3 modes:

* output: midiscriptor produces standard outputs, which can be used using pipes.
* command: midiscriptor subprocesses user defined command.
* keyboard: midiscriptor acts like a computer keyboard