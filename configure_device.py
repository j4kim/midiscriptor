import sys, usb.core, usb.util, subprocess
from pprint import pprint
import json
import pickle

TIMEOUT = 100

CONFIG = {}

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


def select_device():
    global CONFIG
    devices = tuple(usb.core.find(find_all=True))
    print('Here are your connected usb devices: ')

    for i, d in enumerate(devices):
        print ("{}: {} - {}".format(i, d.manufacturer, d.product))

    dev = None
    while not dev:
        n = input('Choose your device (in range [0,%d]): ' % (len(devices)-1))
        try:
            dev = devices[int(n)]
        except:
            print('No device at index', n)

    print('Selected device:', dev.product)
    CONFIG = {
        "device": dev.product,
        "vendor_id": dev.idVendor,
        "product_id": dev.idProduct,
        "mode":"output",
        "actions":{}
    }
    return dev

def print_array(data):
    for i,d in enumerate(data):
        print("[{}]->{}  ".format(i,d), end="")
    print("")

def idfy(data):
    return "{};{};{}".format(data[0], data[1], data[2])

def train(ep):
    print("Now you can try your inputs")
    print("Type CTRL+C to go back to menu")
    print("{:^10}|{:^10}".format("input id","value"))
    print("{:_<10}|{:_<10}".format("",""))
    while True:
        try:
            data = ep.read(4, TIMEOUT)
            input_id = idfy(data)
            print("{:<10}|{:<10}".format(input_id, data[3]))
        except usb.core.USBError as err:
            if err.strerror == 'Operation timed out':
                continue
            else:
                print(err)
                print('Maybe it can help to reconnect your device')
                return
        except KeyboardInterrupt:
            print('')
            break

def configure(ep):
    global CONFIG
    print("Make the input you want to configure")
    print("Type CTRL+C to go back to menu")
    while True:
        try:
            data = ep.read(4, TIMEOUT)
            break
        except usb.core.USBError as err:
            if err.strerror == 'Operation timed out':
                continue
            else:
                print(err)
                print('Maybe it can help to reconnect your device')
                return
        except KeyboardInterrupt:
            break

    input_id = idfy(data)
    choice = input("Configure an action for input {} ? (y/N):".format(input_id))

    if choice == 'y':
        if input_id in CONFIG["actions"]:
            print("Already configured action for this input: '{}'".format(CONFIG["actions"][input_id]))
            if input("Override existing action ? (y/N):".format()) != "y":
                return
        CONFIG["actions"][input_id] = input("Type the command associated to the input:\n")
        print("Input successfully configured")

def mode(ep):
    global CONFIG
    modes = {"o":"output","c":"command","k":"keyboard"}

    s ="Select mode:"
    for k,m in modes.items():
        s += "\n  {} : {} {}".format(k, m.capitalize(), "(selected)" if CONFIG["mode"] == m else "")
    print(s)
    
    choice = "?"
    while choice not in modes:
        choice = input("Mode (default:o): ")
        CONFIG["mode"] = modes.get(choice,"o")

def show(ep):
    global CONFIG
    print("Actual configuration:")
    pprint(CONFIG)

MENU = "\nMenu:\n  q - Quit\n  t - Train\n  c - Configure an input\n  m - Change mode\n  s - Show configuration\n  h - Show this help menu"

FUNCTIONS = {
    't':train,
    'c':configure,
    's':show,
    'm':mode,
    'h':lambda e: print(MENU)
}

def main(config=None):
    global CONFIG

    if config:
        CONFIG = config
        dev = usb.core.find(idVendor=CONFIG["vendor_id"], idProduct=CONFIG["product_id"])
        if dev == None:
            print("Device '{}' not detected".format(CONFIG["device"]))
            return
        print("Configuration loaded")
    else:
        dev = select_device()

    ep = first_endpoint(dev)

    print(MENU)
    choice = ''
    while(True):
        choice = input('> ')
        if choice == 'q':
            break
        elif choice in FUNCTIONS:
            FUNCTIONS[choice](ep)
        elif choice != '':
            print("Unknown command, type m to show menu")
            

    if input('Save configuration? (y/N): ') == 'y':
        filename = input('configuration file name: ') + '.json'
        with open(filename, 'w') as f:
            json.dump(CONFIG, f, indent=4)
            print('Configuration stored in file ' + filename)
    else:
        print("\nkthxbye")


if __name__ == '__main__':

    # load potential config file given in argument
    try:
        config_file = sys.argv[1]
        with open(config_file) as f:
            config = json.loads(f.read())
        main(config)
    except IndexError:
        main()
    except FileNotFoundError:
        print("Configuration file not found")
    except ValueError:
        print("Invalid configuration file")

        

