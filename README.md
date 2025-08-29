# Easily use a Coral TPU from Python

Use the Coral TPU **directly from Python** with no arcane libraries (TFLite, PyCoral, Edge TPU Runtime, or any other dungeon monsters)

![2025-02-01 19 03 07](https://github.com/user-attachments/assets/ae40776b-272b-4c4e-b408-5e2652cd5d54)

❗ Getting rid of all dependencies means that the Coral TPU can be easily integrated with *ANY* device that supports USB.
> Wanna run ML on a RPi Zero? on an ESP32 running MicroPython? On your custom ASIC? If you have USB, you can have ML.

## Requirements:
Your embedded system / single board computer can use the Coral TPU if it supports:
- Python
- USB (via `pyusb`)

**Nothing** else is needed.

<img width="955" alt="Screenshot 2025-03-17 at 01 40 06" src="https://github.com/user-attachments/assets/b7b18830-a5c2-4a7e-857d-509e9892fad4" />

## Quickstart

Install USB library:
```bash
pip install pyusb
```

Prepare input image: resize to 224x224 and transform to bytes:

```python
from PIL import Image
import sys

path = sys.argv[1]

image = Image.open(path).convert('RGB').resize((224, 224))
image_bytes = image.tobytes()

with open(f'{path.split(".")[0]}.bin', 'wb') as binary_file:
    binary_file.write(image_bytes)
```

### Running image classification 

1. `python install_firmware.py`
2. `python inference.py`

### Running object detection

1. `python install_firmware.py`
2. `cd object-detection`
3. `python inference.py`

> **Note:** If your computer supports `Pillow`, you can visualze the bounding boxes after running object detection with:

```python
python object-detection/inference.py my_image.png
```
