from picamera2 import Picamera2, Preview, MappedArray, Transform

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

        # Draw a rectangle
        draw.rectangle([x0, y0, x1, y1], outline=(0, 255, 0), width=2)

        # Draw text
        # You may need to specify a font path or use a default font
        font = ImageFont.load_default()

        # Text to draw
        label = "Hello, World!"

        # Create a new image for the text with a larger size
        text_size = (200, 50)  # Size of the text image
        text_image = Image.new('RGB', text_size, (255, 255, 255))
        text_draw = ImageDraw.Draw(text_image)

        # Draw the text on the new image
        text_draw.text((5, 15), label, fill=(0, 255, 0), font=font)

        # Resize the text image to the desired size
        scaled_text_image = text_image.resize((text_size[0] * 2, text_size[1] * 2), Image.ANTIALIAS)

        # Paste the scaled text image onto the original image
        image.paste(scaled_text_image, (10, 10), scaled_text_image)

        # Convert the PIL Image back to a NumPy array
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
