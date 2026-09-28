"""Create a self-contained image for the later examples."""

from pathlib import Path

import cv2
import numpy as np

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "assets" / "generated" / "sample_scene.png"


def main() -> None:
    image = np.full((480, 720, 3), (35, 40, 45), dtype=np.uint8)
    cv2.rectangle(image, (70, 80), (300, 350), (50, 180, 80), thickness=-1)
    cv2.circle(image, (510, 220), 105, (30, 150, 230), thickness=-1)
    cv2.line(image, (40, 420), (680, 420), (220, 220, 220), thickness=4)
    cv2.putText(image, "OpenCV", (245, 445), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUTPUT_PATH), image):
        raise RuntimeError(f"Could not write image to {OUTPUT_PATH}")
    print(f"Created {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
