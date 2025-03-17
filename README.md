# Coral in Python

Use the Coral TPU directly from Python, without needing other TPU custom libraries (PyCoral, Edge TPU Runtime, TFLite, etc.).

The only requirements to run this software are:
- Python
- USB (via `pyusb`)

<img width="955" alt="Screenshot 2025-03-17 at 01 40 06" src="https://github.com/user-attachments/assets/b7b18830-a5c2-4a7e-857d-509e9892fad4" />

## Getting started

```bash
pip install pyusb
```

## Running classification inference

1. `python install_firmware.py`
2. `python inference.py`

## Running object detection inference

1. `python install_firmware.py`
2. `cd object-detection`
3. `python inference.py`

If your computer has `Pillow` installed, you can visualize the bounding boxes after running inference with:

```python
python inference.py my_image.png
```
