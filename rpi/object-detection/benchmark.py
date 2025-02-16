from PIL import Image
import numpy as np
import time
from inference_object_detection import load_device, load_model, run_inference


# Send model and data
model_data = open("ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite", "rb").read()
image_data = Image.new('RGB', (300, 300)).tobytes()
anchors = np.load('anchors.npy')

dev = load_device()
load_model(dev, model_data)


while True:
    start_time = time.time()
    it=50
    for _ in range(it):
        _ = run_inference(dev, model_data, image_data, anchors)
    end_time = time.time()
    elapsed_time = (end_time - start_time) / it * 1000

    print("Using 'mobilenet_v2_1.0_224_quant_edgetpu.tflite'")
    print(f"Inference: {elapsed_time:.2f} ms/it")
    time.sleep(1)
