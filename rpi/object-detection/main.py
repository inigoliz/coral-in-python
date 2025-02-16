from picamera2 import Picamera2, Preview, MappedArray
from libcamera import Transform

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

from inference_object_detection import load_device, load_model, run_inference


def draw_objects(request):
    with MappedArray(request, "main") as m:
        image = Image.fromarray(m.array)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        wi, hi = image.size # (1280, 960)

        # image.save('fullframe.png')

        # Inference
        lores_img = image.convert('RGB').resize((300, 300))
        # lores_img.save('lw.png')
        lores_image = lores_img.tobytes()

        start_time = time.time()
        # image_data = Image.open("dog.jpg").convert('RGB').resize((300,300)).tobytes()
        objects = run_inference(dev, model_data, lores_image, anchors)
        end_time = time.time()

        # if len(top_five) == 0: top_five.append("")

        # fps = f"{1 / round((end_time - start_time), 4):.0f}"
        # top_class = top_five[0]
        # print(top_class)

        # label = f"{top_class}\n{fps} FPS"

        # Visualization
        draw = ImageDraw.Draw(image)

        for obj in objects:
            xc, yc, w, h = obj['bbox']
            xl = (xc - w / 2) * wi
            xr = (xc + w / 2) * wi
            yl = (yc - h / 2) * hi
            yr = (yc + h / 2) * hi
            print(xl, yl, xr, yr)
            draw.rectangle([xl, yl, xr, yr], outline="red", width=8)  # Box in black

        m.array[:] = np.array(image)

        image.save('jeej.jpg')


# Initialization
fps = 0
top_class = ""
dev = load_device()
model_data = open("ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite", "rb").read()
load_model(dev, model_data)
anchors = np.load("anchors.npy")

# Configure and start Picamera2.
picam2 = Picamera2()
video_w, video_h = 1280, 960
# lores = {'size': (300, 300), 'format': 'XBGR8888'}
main = {'size': (video_w, video_h), 'format': 'BGR888'}
controls = {'FrameRate': 30}
config = picam2.create_preview_configuration(main, controls=controls)
# config = picam2.create_preview_configuration({"size": (video_w, video_h)})
picam2.configure(config)

# picam2.start_preview(Preview.QTGL)
picam2.start()
picam2.pre_callback = draw_objects


time.sleep(400)
# while (loop_end - loop_start) < 2:
#     print('Running')
    # frame = picam2.capture_array('lores')

    # image = Image.fromarray(frame)
    # image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # image.save("tss2.png")

    
    # start_time = time.time()
    # top_five = run_inference(dev, model_data, image_data)
    # end_time = time.time()

    # fps = f"{1 / round((end_time - start_time), 4):.0f}"
    # top_class = top_five[0]

    # print(top_class)
    # loop_end = time.time()

# time.sleep(1)
