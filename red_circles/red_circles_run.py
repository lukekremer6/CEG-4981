import os
import time
from red_circles import find_red_circles

USB_MOUNT_PATH = "/media/admin"
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")
POLL_INTERVAL = 3  # seconds between checks

def get_usb_drives():
    """Return a list of mounted USB drive paths under /media/admin."""
    if not os.path.exists(USB_MOUNT_PATH):
        return []
    drives = [
        os.path.join(USB_MOUNT_PATH, d)
        for d in os.listdir(USB_MOUNT_PATH)
        if os.path.isdir(os.path.join(USB_MOUNT_PATH, d))
    ]
    return drives


def find_images(drive_path):
    """Recursively find all image files on the drive."""
    images = []
    for root, _, files in os.walk(drive_path):
        for f in files:
            if f.lower().endswith(IMAGE_EXTENSIONS):
                images.append(os.path.join(root, f))
    return images


if __name__ == "__main__":
    print("Waiting for USB drive at /media/admin/ ...")
    previous_drives = set()

    while True:
        current_drives = set(get_usb_drives())
        new_drives = current_drives - previous_drives

        if new_drives:
            for drive in new_drives:
                print(f"\nUSB detected: {drive}")
                images = find_images(drive)
                if images:
                    print(f"Found {len(images)} image(s). Processing...")
                    for img_path in images:
                        print(f"  Processing: {img_path}")
                        find_red_circles(img_path)
                    print("Done processing this USB.")
                else:
                    print("No images found on this USB.")

        previous_drives = current_drives
        time.sleep(POLL_INTERVAL)