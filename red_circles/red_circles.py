import cv2
import numpy as np
import os

def find_red_circles(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Could not read image")
        return

    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Red has two separate ranges in the HSV color scheme,
    # so we need two separate masks to detect it.
    lower_red1 = np.array([0, 120, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    os.makedirs("cropped_images", exist_ok=True)

    image_name = os.path.basename(image_path)
    count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # Ignore small circles
        if area < 600 or perimeter == 0:
            continue

        # Calculate how round the circle is
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        # Compare area of circumcircle to area of actual circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        circle_area = np.pi * (radius ** 2)
        fill_ratio = area / circle_area if circle_area > 0 else 0

        # Compare width and height of circle to ignore ovals and ellipses
        _, _, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h if h != 0 else 0

        # Filters
        if (circularity < 0.8
            or fill_ratio < 0.65
            or not (0.7 <= aspect_ratio <= 1.3)):
            continue

        x = int(x)
        y = int(y)
        radius = int(radius) + 10

        x1 = max(0, x - radius)
        y1 = max(0, y - radius)
        x2 = min(image.shape[1], x + radius)
        y2 = min(image.shape[0], y + radius)

        cropped = image[y1:y2, x1:x2]
        output_path = f"cropped_images/cropped_{count}_{image_name}"
        cv2.imwrite(output_path, cropped)
        count += 1

    print(f"Saved {count} red circle(s)")