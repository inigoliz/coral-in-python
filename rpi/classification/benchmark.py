from inference_classification import load_device, load_model, run_inference
from PIL import Image
import time

dev = load_device()

model_data = open("mobilenet_v2_1.0_224_quant_edgetpu.tflite", "rb").read()
image_data = Image.new('RGB', (224, 224)).tobytes()
load_model(dev, model_data)

while True:
    start_time = time.time()
    it=1000
    for _ in range(it):
        _ = run_inference(dev, model_data, image_data)
    end_time = time.time()
    elapsed_time = (end_time - start_time) / it * 1000

    print("Using 'mobilenet_v2_1.0_224_quant_edgetpu.tflite'")
    print(f"Inference: {elapsed_time:.2f} ms/it")
    time.sleep(1)
