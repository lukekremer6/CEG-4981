# Demonstrates red circle detection on sample images.

from red_circles import find_red_circles
import os

if __name__ == "__main__":
    usb_path = r"D:\sampleimages"
    for filename in os.listdir(usb_path):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            path = os.path.join(usb_path, filename).replace("\\", "/")
            find_red_circles(path)