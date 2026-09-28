"""Read, inspect, transform, and save an image."""

from pathlib import Path

import cv2

MODULE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = MODULE_DIR / "assets" / "generated" / "sample_scene.png"
OUTPUT_PATH = MODULE_DIR / "assets" / "generated" / "sample_scene_processed.png"


def main() -> None:
    image = cv2.imread(str(INPUT_PATH))
    if image is None:
        raise FileNotFoundError(f"Run 02_create_sample_image.py first: {INPUT_PATH}")

    print(f"Height, width, channels: {image.shape}")
    print(f"Pixel data type: {image.dtype}")

    resized = cv2.resize(image, (360, 240), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=80, threshold2=160)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUTPUT_PATH), edges):
        raise RuntimeError(f"Could not write image to {OUTPUT_PATH}")
    print(f"Saved edge image: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
