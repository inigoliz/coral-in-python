import argparse

import cv2

from picamera2 import MappedArray, Picamera2, Preview
from picamera2.devices import Hailo

import time


def draw_objects(request):
    with MappedArray(request, "main") as m:
        x0, y0, x1, y1 = 50, 50, 150, 150
        label = f"Hello Video"
        cv2.rectangle(m.array, (x0, y0), (x1, y1), (0, 255, 0, 0), 2)
        cv2.putText(m.array, label, (x0 + 5, y0 + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0, 0), 1, cv2.LINE_AA)


    # Configure and start Picamera2.
picam2 = Picamera2()
# main = {'size': (video_w, video_h), 'format': 'XRGB8888'}
# lores = {'size': (model_w, model_h), 'format': 'RGB888'}
# controls = {'FrameRate': 30}
# config = picam2.create_preview_configuration(main, lores=lores, controls=controls)
# picam2.configure(config)

picam2.start_preview(Preview.QTGL)
picam2.start()
picam2.pre_callback = draw_objects

# Process each low resolution camera frame.
time.sleep(5)