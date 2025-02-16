import PIL.Image
import usb.core
import usb.util
import numpy as np
from math import exp

import sys

import PIL
from hexdump import hexdump

setup = """
libusb_control_transfer(RequestType: 0x80, Request: 0x06, Value: 0x0100, Index: 0x0000, Length:   18) : 00 00 00 81 42 6f 01 00 00 00 70 17 00 00 01 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa30c, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa30c, Index: 0x0001, Length:    4) : 59 00 0f 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa314, Index: 0x0001, Length:    4) : 59 00 0f 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 00 00 00 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 01 00 00 00 
libusb_control_transfer(RequestType: 0x40, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 5c 02 85 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa318, Index: 0x0001, Length:    4) : 5c 02 c5 00 
libusb_control_transfer(RequestType: 0xc0, Request: 0x00, Value: 0x4018, Index: 0x0004, Length:    8) : f0 8a 42 6f 01 00 00 00 
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
libusb_control_transfer(RequestType: 0xc0, Request: 0x01, Value: 0xa33c, Index: 0x0001, Length:    4) : 7f 00 70 00 
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
        print("Did you foget to run 'load_firmware.py'?")
        sys.exit(1)

    dev.reset()
    # time.sleep(0.6)
    usb.util.claim_interface(dev, 0)
    # dev.set_configuration(1)

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
    send_with_header(dev, model_data, start=0x6442dc, length=11472, mysterious_flag=0x0)
    send_with_header(dev, model_data, start=0xafac, length=6523264, mysterious_flag=0x2, subpacket_size=1048576)


def iou(box1, box2):
    """
    box1, box2: [xc, yc, w, h], normalized in [0, 1]
    """
    xc1, yc1, w1, h1 = box1
    xc2, yc2, w2, h2 = box2

    xl1 = xc1 - w1 / 2
    yt1 = yc1 - h1 / 2
    xr1 = xc1 + w1 / 2
    yb1 = yc1 + h1 / 2

    xl2 = xc2 - w2 / 2
    yt2 = yc2 - h2 / 2
    xr2 = xc2 + w2 / 2
    yb2 = yc2 + h2 / 2

    xl = max(xl1, xl2)
    xr = min(xr1, xr2)
    yt = max(yt1, yt2)
    yb = min(yb1, yb2)

    area_inters = (xr - xl) * (yb - yt)
    area1 = w1 * h1
    area2 = w2 * h2

    return 2 * area_inters / (area1 + area2)

def run_inference(dev, model_data, image_data, anchors):

    send_with_header(dev, model_data, start=0x65713c, length=257648, mysterious_flag=0x0)
    send_with_header(dev, image_data, start=0x00, length=270000, mysterious_flag=0x01)

    # for _ in range(5):
    #     _ = dev.read(0x81, 1024)

    send_with_header(dev, model_data, start=0x6551cc, length=7632, mysterious_flag=0x0)


    # Receive activations
    class_activations_rsp = bytearray()
    box_transform_activations_rsp = bytearray()

    # First 8 are the box regression activations
    for _ in range(8):
        rsp = dev.read(0x81, 1024)
        box_transform_activations_rsp.extend(rsp)
        # hexdump(rsp)

    for _ in range(170):
        rsp = dev.read(0x81, 1024)
        # hexdump(rsp1)
        class_activations_rsp.extend(rsp)

    dev.read(0x82, 16)

    for _ in range(4):
        rsp = dev.read(0x81, 1024)
        # hexdump(rsp1)
        class_activations_rsp.extend(rsp)

    # Partition the bytearray into chunks of size 92 (90 classes + background + EOL byte)
    chunk_size = 92
    chunks_classes = [class_activations_rsp[i:i + chunk_size - 1] for i in range(0, len(class_activations_rsp)-chunk_size, chunk_size)]  # remove last element, 0x80, EOL

    chunk_size = 4
    chunks_box_transforms = [box_transform_activations_rsp[i:i + chunk_size] for i in range(0, len(box_transform_activations_rsp)-chunk_size, chunk_size)]

    # Extract max activations
    activation_data = []
    threshold = 0.5
    for index, chunk in enumerate(chunks_classes):
        max_score = max(chunk)
        max_class = chunk.index(max_score)

        if max_class != 0 and max_score/255 > threshold:
            activation = {
                'class': max_class,
                'score': max_score,
                'chunk': index
            }
            activation_data.append(activation)

    # Dequantize and extract bbox
    dequantize = lambda q: 0.09133967012166977 * (q - 179)  # found in the model file
    for activation in activation_data:
        chunk = activation['chunk']
        raw_box_transform = chunks_box_transforms[chunk]
        box_transform = list(map(dequantize, raw_box_transform))

        # Found in the model file
        x_scale = 10
        y_scale = 10
        w_scale = 5
        h_scale = 5

        anchor = anchors[chunk]
        ya, xa, ha, wa = anchor

        ty, tx, th, tw = box_transform

        y = ya + ha * ty / y_scale
        x = xa + wa * tx / x_scale

        h = ha * exp(th / h_scale)
        w = wa * exp(tw / w_scale)
        
        activation['bbox'] = [x, y, w, h]


    # Instead of NMS, keep box with highest score and deduplicate based on IoU
    objects = []

    def get_obj_with_class(objects, class_value):
        is_of_class_value = lambda obj: obj['class'] == class_value
        return list(filter(is_of_class_value, objects))

    for act in activation_data:
        act_class = act['class']
        act_score = act['score']
        act_bbox = act['bbox'] 

        obj_matching_class = get_obj_with_class(objects, act_class)

        if len(obj_matching_class) == 0:
            objects.append(act)
            continue

        for obj in obj_matching_class:
            obj_class = obj['class']
            obj_score = obj['score']
            obj_bbox = obj['bbox']

            iou_threshold = 0.8
            if iou(act_bbox, obj_bbox) > iou_threshold and act_score > obj_score:
                obj['bbox'] = act['bbox']
                obj['score'] = act['score']

        if all([(iou(act_bbox, obj['bbox']) < iou_threshold) for obj in objects]):
            objects.append(act)

    return objects