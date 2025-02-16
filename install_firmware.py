import usb.core
import time


def send_firmware():
    fw = open("apex_latest_single_ep.bin", "rb").read()
    it = 0
    for i in range(0, len(fw), 0x100):
        dev.ctrl_transfer(0x21, 0x01, it, 0, fw[i:i+0x100])
        dev.ctrl_transfer(0xa1, 0x03, 0, 0, 6)
        it += 1
        

dev = usb.core.find(idVendor=0x18d1, idProduct=0x9302)
if (dev == None):
    print("Downloading firmware...")
    dev = usb.core.find(idVendor=0x1a6e, idProduct=0x089a)
    dev.reset()

    hex_data = [0x00, 0x00, 0x00, 0xcb, 0xea, 0x6e, 0x01, 0x00, 0x00, 0x00, 0x70, 0x17, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00]
    dev.ctrl_transfer(0x80, 0x06, 0x100, 0x00, bytearray(hex_data))
    dev.ctrl_transfer(0x80, 0x06, 0x200, 0x00, 521)

    send_firmware()

    dev.ctrl_transfer(0x21, 0x01, 0x2b, 0x00, 0)
    dev.ctrl_transfer(0xa1, 0x03, 0x00, 0x00, 6)

    try: 
        dev.reset()
    except usb.core.USBError:
        print("Resetting...")
    time.sleep(4)

    dev = usb.core.find(idVendor=0x18d1, idProduct=0x9302)
    if(dev):
        print("Firmware downloaded correctly.")
