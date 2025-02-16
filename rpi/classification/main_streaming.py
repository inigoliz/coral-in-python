import http.server
import socketserver
import io
import time
import numpy as np
from PIL import Image, ImageDraw
from picamera2 import Picamera2, MappedArray

from inference_classification import load_device, load_model, run_inference


# Function to process the image
def draw_objects(request):
    global last_processed_image  # Use global variable to store the processed image

    with MappedArray(request, "main") as m:
        image = Image.fromarray(m.array)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        wi, hi = image.size  # (1280, 960)

        # Inference (Placeholder for your actual inference function)
        lores_img = image.convert('RGB').resize((300, 300))
        lores_image = lores_img.tobytes()

        start_time = time.time()
        objects = run_inference(dev, model_data, lores_image, anchors)
        end_time = time.time()

        # Visualization
        draw = ImageDraw.Draw(image)
        for obj in objects:
            xc, yc, w, h = obj['bbox']
            xl = (xc - w / 2) * wi
            xr = (xc + w / 2) * wi
            yl = (yc - h / 2) * hi
            yr = (yc + h / 2) * hi
            draw.rectangle([xl, yl, xr, yr], outline="red", width=8)  # Draw bounding box

        
        # image.save("theimg.jpg")
        # Save the modified image to the global variable
        output = io.BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)
        last_processed_image = output.getvalue()  # Store the processed image in the global variable

        m.array[:] = np.array(image)


class StreamingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/video_feed':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            while True:
                # Stream the last processed image
                if last_processed_image is not None:
                    self.wfile.write(b'--frame\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', str(len(last_processed_image)))
                    self.end_headers()
                    self.wfile.write(last_processed_image)
                    self.wfile.flush()
        else:
            self.send_response(404)
            self.end_headers()


# Initialize Coral
fps = 0
top_class = ""
dev = load_device()
model_data = open("ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite", "rb").read()
load_model(dev, model_data)
anchors = np.load("anchors.npy")

# Initialize the camera
picam2 = Picamera2()
video_w, video_h = 1280, 960
main = {'size': (video_w, video_h), 'format': 'BGR888'}
controls = {'FrameRate': 30}
config = picam2.create_preview_configuration(main, controls=controls)
picam2.configure(config)

# picam2.start_preview(Preview.QTGL)
picam2.start()
picam2.pre_callback = draw_objects

# Global variable to hold the last processed image
last_processed_image = None


# Set up the server
PORT = 8000
with socketserver.TCPServer(("", PORT), StreamingHandler) as httpd:
    print(f"Serving on port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
