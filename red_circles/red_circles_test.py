# Demonstrates red circle detection on sample images.

import os
from red_circles import find_red_circles

if __name__ == "__main__":
    usb_path = "test_images"
    for filename in os.listdir(usb_path):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            path = os.path.join(usb_path, filename).replace("\\", "/")
            find_red_circles(path)