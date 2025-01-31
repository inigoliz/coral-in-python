from picamera2 import Picamera2, Preview
# import cv2
import time


# def draw_objects(request):
#     with MappedArray(request, "main") as m:
#         label = f"Hola"
#         cv2.rectangle(m.array, (20, 20), (150, 150), (0, 255, 0, 0), 2)
#         cv2.putText(m.array, label, (10 + 5, 10 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0, 0), 1, cv2.LINE_AA)

                
def main():
    # video_w, video_h = 1280, 960
    # model_w, model_h = 300, 300

    picam2 = Picamera2()
    # main = {'size': (video_w, video_h), 'format': 'XRGB8888'}
    # lores = {'size': (model_w, model_h), 'format': 'RGB888'}
    # controls = {'FrameRate': 30}
    config = picam2.create_preview_configuration()
    # config = picam2.create_preview_configuration(main, lores=lores, controls=controls)
    picam2.configure(config)
    picam2.start_preview(Preview.QTGL)

    # picam2.start_preview(Preview.QTGL, x=0, y=0, width=800, height=600)
    picam2.start()
    time.sleep(5)
    # picam2.pre_callback = draw_objects

    # Process each low resolution camera frame.
    #while True:
    #    print('hi')
    #     frame = picam2.capture_array('lores')

    #     # Run inference on the preprocessed frame
    #     results = hailo.run(frame)

    #     # Extract detections from the inference results
    #     detections = extract_detections(results, video_w, video_h, class_names, args.score_thresh)


if __name__ == '__main__':
    main()