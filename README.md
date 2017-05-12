# midiscriptor
Control your Linux system with MIDI devices


## Requirements

* Python 3
* PyUSB
* PyUserInput ?
* A MIDI-USB device (tested on Akai LPD8)

## Installation

Follow the instructions in the [PyUSB repository](https://github.com/walac/pyusb#installing-pyusb-on-gnulinux-systems)

## User guide

3 modes:

* output: midiscriptor produces standard outputs, which can be used using pipes.
* command: midiscriptor subprocesses user defined command.
* keyboard: midiscriptor acts like a computer keyboard