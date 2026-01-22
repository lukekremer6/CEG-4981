# Demonstrates red circle detection on sample images.

from red_circles import find_red_circles

if __name__ == "__main__":
    test_images = [
        "test_images/image1.png",
        "test_images/image2.png",
        "test_images/image9.png",
        "test_images/image13.png",
        "test_images/image35.png",
        "test_images/rand2.png",
        "test_images/rand3.jpeg",
        "test_images/rand4.jpeg",
        "test_images/rand5.jpeg",
        "test_images/rand6.jpeg",
        "test_images/rand7.jpg",
        "test_images/rand8.jpeg",
        "test_images/rand9.jpeg",
        "test_images/The_Death_Star.png",
    ]

    for image in test_images:
        find_red_circles(image)
