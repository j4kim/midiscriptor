import sys, usb.core, usb.util, json
import subprocess

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

def print_array(data):
    for i,d in enumerate(data):
        print("[{}]->{}  ".format(i,d), end="")
    print("")

def idfy(data):
    return "{};{};{}".format(data[0], data[1], data[2])

def main(config):
    dev = usb.core.find(idVendor=config["vendor_id"])
    ep = first_endpoint(dev)
    print("midiscriptor is running")
    while True:
        try:
            data = ep.read(4, TIMEOUT)
            input_id = idfy(data)
            if input_id in config["actions"]:
                print("**********************")
                command = config["actions"][input_id]
                print("subprocess command '{}'".format(command))
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                if output:
                    print(output.decode('utf-8'))
                if error:
                    print(error.decode('utf-8'), file=sys.stderr)
            else:
                print("no action configured for input '%s'" % input_id, file=sys.stderr)
                print_array(data)
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
        print("Configuration file not found")
    except ValueError:
        print("Invalid configuration file")

