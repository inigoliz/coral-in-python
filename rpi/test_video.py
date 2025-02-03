from picamera2 import Picamera2, Preview, MappedArray
from libcamera import Transform

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time

def draw_objects(request):
    with MappedArray(request, "main") as m:
        # Convert the array to a PIL Image
        image = Image.fromarray(m.array)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        # print(image.size)
        # image.save('image.png')  # Specify the file path and format

        # Create a draw object
        draw = ImageDraw.Draw(image)

        # Define rectangle coordinates and label
        x0, y0, x1, y1 = 50, 50, 250, 250
        label = "Hello Video"

        draw.rectangle([x0, y0, x1, y1], outline=(0, 255, 0), width=5)

        # Load the default font
        font = ImageFont.load_default()
        fontsize = 24

        # Create a new image to hold the text
        text_size = (fontsize * len(label), fontsize)
        text_size = draw.textsize(label, font=font)
        text_image = Image.new("RGB", text_size, (255, 255, 255))  # Transparent background
        text_draw = ImageDraw.Draw(text_image)

        # Draw the text on the new image
        text_draw.text((0, 0), label, fill=(0, 255, 0), font=font)

        # Scale the text image
        scale_factor = 2  # Adjust this factor to make the text larger
        scaled_text_image = text_image.resize((text_size[0] * scale_factor, text_size[1] * scale_factor), Image.ANTIALIAS)

        # Paste the scaled text image onto the original image
        text_position = (x0 + 5, y0 + 15)  # Position where the text should be pasted
        image.paste(scaled_text_image, text_position, scaled_text_image)

        m.array[:] = np.array(image)

# Configure and start Picamera2.
picam2 = Picamera2()
video_w, video_h = 1280, 960
main = {'size': (video_w, video_h), 'format': 'XRGB8888'}
# lores = {'size': (300, 300), 'format': 'BGR888'}
controls = {'FrameRate': 30}
config = picam2.create_preview_configuration(main, controls=controls)
picam2.configure(config)

picam2.start_preview(Preview.QTGL)
picam2.start()
picam2.pre_callback = draw_objects

# Process each low resolution camera frame.
time.sleep(5)
