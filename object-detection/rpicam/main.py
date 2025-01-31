from picamera2 import MappedArray, Picamera2, Preview

def main():
    video_w, video_h = 1280, 960
    model_w, model_h = 300, 300

    with Picamera2() as picam2:
        main = {'size': (video_w, video_h), 'format': 'XRGB8888'}
        lores = {'size': (model_w, model_h), 'format': 'RGB888'}
        controls = {'FrameRate': 30}
        config = picam2.create_preview_configuration(main, lores=lores, controls=controls)
        picam2.configure(config)

        picam2.start_preview(Preview.QTGL, x=0, y=0, width=video_w, height=video_h)
        picam2.start()
        # picam2.pre_callback = draw_objects

        # Process each low resolution camera frame.
        # while True:
        #     frame = picam2.capture_array('lores')

        #     # Run inference on the preprocessed frame
        #     results = hailo.run(frame)

        #     # Extract detections from the inference results
        #     detections = extract_detections(results, video_w, video_h, class_names, args.score_thresh)


if __name__ == '__main__':
    main()