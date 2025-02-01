from picamera2 import Picamera2
import numpy as np
import cv2
from PIL import Image

from inference_only_python import load_device, load_model, run_inference

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start(show_preview=True)


model_data = open("mobilenet_v2_1.0_224_quant_edgetpu.tflite", "rb").read()
image_data = Image.open("mug.jpg").convert('RGB').resize((224,224)).tobytes()

dev = load_device()
load_model(dev, model_data)
# while True:
overlay = np.zeros((300, 400, 4), dtype=np.uint8)
overlay[:150, 200:] = (255, 0, 0, 64) # reddish
overlay[150:, :200] = (0, 255, 0, 64) # greenish
overlay[150:, 200:] = (0, 0, 255, 64) # blueish
top_five = run_inference(dev, model_data, image_data)

picam2.set_overlay(overlay)