import cv2
import numpy as np
import os
import math

def find_red_circles(image_path):
    """
    Detect red circles in the given image.
    If it detects a red circle, it generates an
    image file called "cropped_{count}_{image_name}" containing
    the contents of the image inside the red circle.
    It stores this image in a directory called "cropped_images."

    :param image_path: A path to an image file.
    """

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

    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    os.makedirs("cropped_images", exist_ok=True)

    image_name = os.path.basename(image_path)
    count = 0

    if hierarchy is not None:
        for contour, level in zip(contours, hierarchy[0]):
            # Check if contour has a child contour

            if level[2] > 0:
                childContour = contours[level[2]]
                area = cv2.contourArea(contour)
                childArea = cv2.contourArea(childContour)
                perimeter = cv2.arcLength(contour, True)
                childPerimeter = cv2.arcLength(childContour, True)

                # Ignore small circles
                if (area < 600
                    or perimeter == 0
                    or childArea < 300
                    or childPerimeter == 0):
                    continue

                # Calculate how round the circle is
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                childCircularity = 4 * np.pi * childArea / (childPerimeter * childPerimeter)

                # Compare area of circumcircle to area of actual circle
                (x, y), radius = cv2.minEnclosingCircle(contour)
                (_, _), childRadius = cv2.minEnclosingCircle(childContour)
                circle_area = np.pi * (radius ** 2)
                child_circle_area = np.pi * (childRadius ** 2)
                fill_ratio = area / circle_area if circle_area > 0 else 0
                child_fill_ratio = childArea / child_circle_area if child_circle_area > 0 else 0

                # Compare width and height of circle to ignore ovals and ellipses
                _, _, w, h = cv2.boundingRect(contour)
                _, _, childw, childh = cv2.boundingRect(childContour)
                aspect_ratio = w / h if h != 0 else 0
                child_aspect_ratio = childw / childh if childh != 0 else 0

                # Filters
                if (circularity < 0.8
                    or fill_ratio < 0.65
                    or not 0.7 <= aspect_ratio <= 1.3
                    or childCircularity < 0.8
                    or child_fill_ratio < 0.65
                    or not 0.7 <= child_aspect_ratio <= 1.3
                    or math.sqrt(childArea) < math.sqrt(area) * 0.6):
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