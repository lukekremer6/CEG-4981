import cv2
import numpy as np

def find_red_circles(image_path):
    """
    Detect red circles in the given image.
    If it detects a red circle, it generates an
    image file called "cropped_{image_name}" containing
    the contents of the image inside the red circle.
    It stores this image in a directory called "cropped_images."

    :param image_path: A path to an image file.
    """

    image = cv2.imread(image_path)

    blurred_image = cv2.blur(image, (3, 3))

    image_hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    # Red has two separate ranges in the HSV color scheme,
    # so we need two separate masks to detect it.
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(image_hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(image_hsv, lower_red2, upper_red2)
    red_mask = mask1 + mask2
    red_image = cv2.bitwise_and(image, image, mask=red_mask)

    _, _, gray = cv2.split(red_image)

    rows = gray.shape[0]
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1,
        rows / 8,
        param1=100,
        param2=30,
        minRadius=0,
        maxRadius=0
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        x, y, r = circles[0][0]
        buffer = 10
        r += buffer
        cropped_image = image[y - r: y + r, x - r : x + r]
        image_name = image_path.split("/")[-1]
        cv2.imwrite("cropped_images/cropped_" + image_name, cropped_image)
