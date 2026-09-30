"""Detect prominent straight edges in a real building photograph."""

from math import pi
from pathlib import Path

import cv2

MODULE_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = MODULE_DIR / "assets" / "input" / "building.jpg"
OUTPUT_PATH = MODULE_DIR / "outputs" / "hough_lines.png"


def main() -> None:
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read input image: {IMAGE_PATH}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 60, 160)
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=pi / 180,
        threshold=80,
        minLineLength=60,
        maxLineGap=12,
    )

    result = image.copy()
    line_count = 0 if lines is None else len(lines)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 2, cv2.LINE_AA)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUTPUT_PATH), result):
        raise RuntimeError(f"Could not write output image: {OUTPUT_PATH}")
    print(f"Detected {line_count} line segments.")
    print(f"Saved result: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()