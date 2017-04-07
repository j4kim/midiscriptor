import sys, usb.core, usb.util


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
    devices = tuple(usb.core.find(find_all=True))
    print('Here are your connected usb devices: ')

    for i, d in enumerate(devices):
        print ([i, d.manufacturer, d.product])

    dev = None
    while not dev:
        n = input('Choose your device (in range [0,%d]): ' % (len(devices)-1))
        try:
            dev = devices[int(n)]
        except:
            print('No device at index', n)

    print('selected device:', dev.product)
    return dev


def get_quit_key(ep):
    print("Hit the control which will close the program")
    while True:
        try:
            data = ep.read(4)
            quit_key = (data[0], data[2])
            print("Quit key set : {}".format(quit_key))
            return quit_key
        except usb.core.USBError as err:
            if err.strerror == 'Operation timed out':
                continue
    


def main():
    dev = select_device()


    ep = first_endpoint(dev)

    print('')
    quit_key = get_quit_key(ep)
    print('')
    print("You can test your controls now")
    print("Hit the quit-control you just set to close")
    
    while True:
        try:
            data = ep.read(4)
            print(data)
            if (data[0], data[2]) == quit_key: break
        except usb.core.USBError as err:
            if err.strerror == 'Operation timed out':
                continue

    print("bye")


if __name__ == '__main__':
    main()




