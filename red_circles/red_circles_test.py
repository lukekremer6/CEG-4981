# Demonstrates red circle detection on sample images.

from red_circles import find_red_circles

if __name__ == "__main__":
    test_images = [
        "test_images/image1.png",
        "test_images/image2.png",
        "test_images/image9.png",
        "test_images/image13.png",
        "test_images/image35.png"
    ]

    for image in test_images:
        find_red_circles(image)
