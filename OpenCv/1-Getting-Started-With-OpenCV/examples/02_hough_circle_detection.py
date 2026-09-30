"""Detect circular objects in a real photograph of colorful candies."""

from pathlib import Path

import cv2
import numpy as np

MODULE_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = MODULE_DIR / "assets" / "input" / "smarties.png"
OUTPUT_PATH = MODULE_DIR / "outputs" / "hough_circles.png"


def main() -> None:
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read input image: {IMAGE_PATH}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=35,
        param1=120,
        param2=35,
        minRadius=15,
        maxRadius=70,
    )

    result = image.copy()
    circle_count = 0 if circles is None else circles.shape[1]
    if circles is not None:
        for x, y, radius in np.rint(circles[0]).astype(int):
            cv2.circle(result, (x, y), radius, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.circle(result, (x, y), 2, (0, 0, 255), 3, cv2.LINE_AA)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUTPUT_PATH), result):
        raise RuntimeError(f"Could not write output image: {OUTPUT_PATH}")
    print(f"Detected {circle_count} circles.")
    print(f"Saved result: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()