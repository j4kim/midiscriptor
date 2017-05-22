import sys, usb.core, usb.util, json

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
    print("{}:{}".format(input_id, value))
    sys.stdout.flush() # pour empecher le buffering et envoyer les données au pipe

def execute_k(input_id, value, actions):
    keyboard = PyKeyboard()
    if input_id in actions:
        copy(actions[input_id])
        keyboard.press_key(keyboard.shift_key)
        keyboard.tap_key(keyboard.insert_key)
        keyboard.release_key(keyboard.shift_key)
        
def calibrate(command, value):
    # recherche dans la commande les chose du genre {{0:100}}
    # qui doivent être remplacées par une valeur entre 0 et 100 selon la valeur de l'input
    m = re.findall(r"{{\d+:\d+}}", command)
    if m:
        a, b = re.findall(r"\d+", m[0]) # a:"0", b:"100" dans notre exemple
        a, b = int(a), int(b)
        value = int((b-a)/127*value+a) # calibrage [0,127] -> [a,b]
        command = re.sub(r"{{.*}}", str(value), command) # remplace {{...}} par la valeur calibrée
    return command

def execute_c(input_id, value, actions):
    if input_id in actions:
        print("**********************")
        command = calibrate(actions[input_id], value)
        print("subprocessing command '{}'".format(command))
        try:
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if output:
                print(output.decode('utf-8'))
            if error:
                print(error.decode('utf-8'), file=sys.stderr)
        except Exception as e:
            print(e)

def main(config):
    dev = usb.core.find(idVendor=config["vendor_id"], idProduct=config["product_id"])
    if dev == None:
        print("Device '{}' not detected".format(config["device"]))
        return
    ep = first_endpoint(dev)
    
    if config["mode"] == "keyboard":
        from pykeyboard import PyKeyboard
        from pyperclip import copy
        execute = execute_k
    elif config["mode"] == "command":
        import subprocess, re
        execute = execute_c
    else:
        config["mode"] = "output"
        execute = execute_o
        
    print("midiscriptor is running in {} mode".format(config["mode"]))
    
    while True:
        try:
            data = ep.read(4, TIMEOUT)
            input_id, value = idfy(data)
            execute(input_id, value, config["actions"])
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
