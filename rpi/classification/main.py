from picamera2 import Picamera2
import numpy as np
import time
from PIL import Image
import cv2

from inference_only_python import load_device, load_model, run_inference


model_data = open("mobilenet_v2_1.0_224_quant_edgetpu.tflite", "rb").read()
image_data = Image.open("mug.jpg").convert('RGB').resize((224,224)).tobytes()

dev = load_device()
load_model(dev, model_data)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration())
picam2.start(show_preview=True)
start = time.time()
end = start
while (end - start) < 5:
    # top_five = run_inference(dev, model_data, image_data)
    overlay = np.zeros((300, 400, 4), dtype=np.uint8)
    # overlay[:150, 200:] = (255, 0, 0, 64) # reddish
    # overlay[150:, :200] = (0, 255, 0, 64) # greenish
    # overlay[150:, 200:] = (0, 0, 255, 64) # blueish

    # overlay_bgra = cv2.cvtColor(overlay, cv2.COLOR_RGBA2BGRA)

    # # Define the text parameters
    # text = "Hello, World!"
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # font_scale = 1
    # font_color = (255, 255, 255, 255)  # White text in BGRA
    # thickness = 2
    # line_type = cv2.LINE_AA

    # # Get the text size to center it
    # (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # # Calculate the text position
    # text_x = (overlay_bgra.shape[1] - text_width) // 2
    # text_y = (overlay_bgra.shape[0] + text_height) // 2

    # # Overlay the text onto the image
    # cv2.putText(overlay_bgra, text, (text_x, text_y), font, font_scale, font_color, thickness, line_type)

    # # Convert back to the original RGBA format
    # overlay_with_text = cv2.cvtColor(overlay_bgra, cv2.COLOR_BGRA2RGBA)

    picam2.set_overlay(overlay)
    end = time.time()
