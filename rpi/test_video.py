from picamera2 import Picamera2, Preview, MappedArray\
from libcamera import Transform

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

def draw_objects(request):
    with MappedArray(request, "lores") as m:
        # Convert the array to a PIL Image
        image = Image.fromarray(m.array)
        print(image.size)
        image.save('image.png')  # Specify the file path and format

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Define rectangle coordinates and label
        x0, y0, x1, y1 = 50, 50, 150, 150
        label = "Hello Video"

        draw.rectangle([x0, y0, x1, y1], outline=(0, 255, 0), width=2)

        font = ImageFont.load_default()
        draw.text((x0 + 5, y0 + 15), label, fill=(0, 255, 0), font=font)

        m.array[:] = np.array(image)

# Configure and start Picamera2.
picam2 = Picamera2()
video_w, video_h = 640, 480
main = {'size': (video_w, video_h), 'format': 'XRGB8888'}
lores = {'size': (300, 300), 'format': 'BGR888'}
controls = {'FrameRate': 30}
config = picam2.create_preview_configuration(main, lores=lores, controls=controls)
picam2.configure(config)

picam2.start_preview(Preview.QTGL, transform=Transform(vflip=1))
picam2.start()
picam2.pre_callback = draw_objects

# Process each low resolution camera frame.
time.sleep(5)
