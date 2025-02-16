import usb.core
import usb.util

import sys

from PIL import Image
from hexdump import hexdump

setup = """
libusb_control_transfer(RequestType: 0x80, Request: 0x06, Value: 0x0100, Index: 0x0000, Length:   18) : 00 00 00 86 53 6d 01 00 00 00 70 17 00 00 01 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa30c, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa30c, Index: 0x0001, Length:    4) : 59 00 0f 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa314, Index: 0x0001, Length:    4) : 59 00 0f 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 04 00 c5 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 04 00 85 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0x907c, Index: 0x0001, Length:    4) : 0f 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0x907c, Index: 0x0001, Length:    4) : 00 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 5c 02 85 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 5c 02 c5 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x00, Value: 0x4018, Index: 0x0004, Length:    8) : 40 90 53 6d 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xa000, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x8788, Index: 0x0004, Length:    8) : 7f 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x00, Value: 0x8788, Index: 0x0004, Length:    8) : 00 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0020, Index: 0x0004, Length:    8) : 02 1e 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa314, Index: 0x0001, Length:    4) : 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa314, Index: 0x0001, Length:    4) : 00 00 15 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa000, Index: 0x0001, Length:    4) : 00 60 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc148, Index: 0x0004, Length:    8) : f0 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc160, Index: 0x0004, Length:    8) : 00 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc058, Index: 0x0004, Length:    8) : 80 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x4018, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x4158, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x4198, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x41d8, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x4218, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x8788, Index: 0x0004, Length:    8) : 7f 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x00, Value: 0x8788, Index: 0x0004, Length:    8) : 08 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x00c0, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0150, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0110, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0250, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0298, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x02e0, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0328, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0190, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x01d0, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0x0210, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc060, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc070, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc080, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc090, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x00, Value: 0xc0a0, Index: 0x0004, Length:    8) : 01 00 00 00 00 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa0d4, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa0d4, Index: 0x0001, Length:    4) : 01 00 00 80 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa704, Index: 0x0001, Length:    4) : 00 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa704, Index: 0x0001, Length:    4) : 7f 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa33c, Index: 0x0001, Length:    4) : 7f 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa33c, Index: 0x0001, Length:    4) : 3f 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa500, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa600, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa558, Index: 0x0001, Length:    4) : 03 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa658, Index: 0x0001, Length:    4) : 03 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa0d8, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa0d8, Index: 0x0001, Length:    4) : 00 00 00 80
"""

def load_device():
    # Assumes device already initialized
    dev = usb.core.find(idVendor=0x18d1, idProduct=0x9302)

    if dev is None:
        print("Device not initialized correctly")
        sys.exit(1)

    dev.reset()
    # time.sleep(0.6)
    usb.util.claim_interface(dev, 0)

    # Send initialization code
    lines = setup.strip().replace(",", "").replace(")", "").split('\n')
    for line in lines:
        line_pieces = line.split()
        # print(line_pieces)
        request_type = int(line_pieces[1], 16)
        request = int(line_pieces[3], 16)
        value = int(line_pieces[5], 16)
        index = int(line_pieces[7], 16)
        length = int(line_pieces[9])

        hex_part = line.split(':')[-1]
        hex_bytes = hex_part.strip().split()
        data = bytearray(int(byte, 16) for byte in hex_bytes)

        _ = dev.ctrl_transfer(request_type, request, value, index, data)

    return dev



def send_with_header(dev, data, start, length, mysterious_flag, subpacket_size=None):
    def craft_header(num, mysterious_flag):
        byte_array = bytearray(num.to_bytes(8, byteorder='little'))
        byte_array[4] = mysterious_flag
        return byte_array

    def _recursive_send_packet(dev, data, start, remaining, subpacket_size):
        if remaining < subpacket_size:
            actual_size = remaining
        else:
            actual_size = subpacket_size

        # actual data
        dev.write(0x01, data[start:start+actual_size])
        if (remaining - actual_size) > 0:
            _recursive_send_packet(dev, data, start=start + actual_size, remaining=remaining - actual_size, subpacket_size=subpacket_size)

    if subpacket_size == None: subpacket_size = length

    # send header
    header = craft_header(num=length, mysterious_flag=mysterious_flag)
    dev.write(0x01, header)

    _recursive_send_packet(dev, data, start, remaining=length, subpacket_size=subpacket_size)


def load_model(dev, model_data):
    send_with_header(dev, model_data, start=0x3c7c8c, length=10064, mysterious_flag=0x0)
    send_with_header(dev, model_data, start=0x33dc, length=3949120, mysterious_flag=0x2, subpacket_size=1048576)
    
def run_inference(dev, model_data, image_data):
    send_with_header(dev, model_data, start=0x3cf4bc, length=261920, mysterious_flag=0x0)
    send_with_header(dev, image_data, start=0x00, length=150528, mysterious_flag=0x01)
    send_with_header(dev, model_data, start=0x3ccbc8, length=10224, mysterious_flag=0x0)

    rsp1 = dev.read(0x82, 16)
    activations = dev.read(0x81, 1024)


    threshold = 100
    with open('imagenet_labels.txt') as file:
        classes = file.readlines()
        sorted_classes = [classes[i] for i in list(sorted(range(len(activations)), key=lambda i: activations[i], reverse=True))[0:5] if activations[i] > threshold]

    return sorted_classes


