import argparse
import os
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = ROOT / "lab-01" / "activity_04_image_filtering" / "image.png"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def save_or_show(window_name: str, image: np.ndarray, filename: str, show: bool) -> None:
    cv2.imwrite(str(OUTPUT_DIR / filename), image)
    if show:
        cv2.imshow(window_name, image)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare multiple edge detection methods in OpenCV.")
    parser.add_argument("--show", action="store_true", help="Display windows interactively after saving results.")
    args = parser.parse_args()

    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel_magnitude = cv2.magnitude(sobel_x, sobel_y)
    sobel_magnitude = cv2.convertScaleAbs(sobel_magnitude)

    laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
    laplacian = cv2.convertScaleAbs(laplacian)

    canny = cv2.Canny(blurred, 50, 150)

    save_or_show("Original", image, "01_original.png", args.show)
    save_or_show("Gray", gray, "02_grayscale.png", args.show)
    save_or_show("Sobel X", cv2.convertScaleAbs(sobel_x), "03_sobel_x.png", args.show)
    save_or_show("Sobel Y", cv2.convertScaleAbs(sobel_y), "04_sobel_y.png", args.show)
    save_or_show("Sobel Magnitude", sobel_magnitude, "05_sobel_magnitude.png", args.show)
    save_or_show("Laplacian", laplacian, "06_laplacian.png", args.show)
    save_or_show("Canny", canny, "07_canny.png", args.show)

    print("Edge detection results saved in:", OUTPUT_DIR)
    print("Methods used:")
    print("- Sobel X: highlights vertical gradients")
    print("- Sobel Y: highlights horizontal gradients")
    print("- Sobel Magnitude: combines both gradient directions")
    print("- Laplacian: second-derivative edge detection")
    print("- Canny: robust edge detection with noise reduction and thresholding")

    if args.show:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
