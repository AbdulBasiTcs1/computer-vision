"""Detect orange regions in the generated sample scene."""

from pathlib import Path

import cv2
import numpy as np

MODULE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = MODULE_DIR / "assets" / "generated" / "sample_scene.png"
OUTPUT_PATH = MODULE_DIR / "assets" / "generated" / "color_detection.png"
LOWER_HSV = np.array([5, 80, 80])
UPPER_HSV = np.array([25, 255, 255])
MIN_CONTOUR_AREA = 500


def main() -> None:
    image = cv2.imread(str(INPUT_PATH))
    if image is None:
        raise FileNotFoundError(f"Run 02_create_sample_image.py first: {INPUT_PATH}")

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, LOWER_HSV, UPPER_HSV)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected = 0
    for contour in contours:
        if cv2.contourArea(contour) < MIN_CONTOUR_AREA:
            continue
        x, y, width, height = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + width, y + height), (255, 255, 255), 2)
        cv2.putText(image, "orange object", (x, max(y - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        detected += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUTPUT_PATH), image):
        raise RuntimeError(f"Could not write image to {OUTPUT_PATH}")
    print(f"Detected {detected} object(s); saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
