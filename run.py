import sys, usb.core, usb.util, json
import subprocess
from pykeyboard import PyKeyboard
from pyperclip import copy

keyboard = PyKeyboard()
TIMEOUT = 100

def claim(dev, interface):
    # if the OS kernel already claimed the device, which is most likely true
    # thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
    if dev.is_kernel_driver_active(interface):
        # tell the kernel to detach
        dev.detach_kernel_driver(interface)
        # claim the device
        usb.util.claim_interface(dev, interface)


def first_endpoint(dev, direction = usb.util.ENDPOINT_IN):
    cfg = dev.get_active_configuration()
    # iterate interfaces
    for i in cfg:
        # iterate endpoints on this interface
        for e in i:
            # get the first IN endpoint
            if(usb.util.endpoint_direction(e.bEndpointAddress) == direction):
                claim(dev, i.bInterfaceNumber)
                return e

def idfy(data):
    input_id = "{};{};{}".format(data[0], data[1], data[2])
    return (input_id, data[3])


def execute_o(input_id, value, actions):
    input_id, value = idfy(data)
    print("{}:{}".format(input_id, value))
    sys.stdout.flush() # pour empecher le buffering et envoyer les données au pipe

def execute_k(input_id, value, actions):
    if input_id in actions:
        copy(actions[input_id])
        keyboard.press_key(keyboard.shift_key)
        keyboard.tap_key(keyboard.insert_key)
        keyboard.release_key(keyboard.shift_key)

def execute_c(input_id, value, actions):
    if input_id in actions:
        print("**********************")
        command = actions[input_id]
        print("subprocessing command '{}'".format(command))
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if output:
            print(output.decode('utf-8'))
        if error:
            print(error.decode('utf-8'), file=sys.stderr)

functions = {
    "output": execute_o,
    "keyboard": execute_k,
    "command": execute_c
}


def main(config):
    dev = usb.core.find(idVendor=config["vendor_id"], idProduct=config["product_id"])
    if dev == None:
        print("Device '{}' not detected".format(config["device"]))
        return
    ep = first_endpoint(dev)
    print("midiscriptor is running")
    while True:
        try:
            data = ep.read(4, TIMEOUT)
            input_id, value = idfy(data)
            functions[config["mode"]](input_id, value, config["actions"])
        except usb.core.USBError as err:
            if err.strerror == 'Operation timed out':
                continue
            else:
                print(err, file=sys.stdout)
                print('Maybe it can help to reconnect your device', file=sys.stderr)
                return
        except KeyboardInterrupt:
            break
        


if __name__ == '__main__':
    try:
        config_file = sys.argv[1]
        with open(config_file) as f:
            config = json.loads(f.read())
        main(config)
    except IndexError:
        print("No configuration file given")
    except FileNotFoundError:
        print("File not found")
    except ValueError:
        print("Invalid configuration file")
