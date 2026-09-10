"""Lab Task 1: Basic image operations for five input images."""

from pathlib import Path

import cv2


TASK_DIR = Path(__file__).resolve().parent
INPUT_DIR = TASK_DIR / "input"
OUTPUT_DIR = TASK_DIR / "output"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def process_image(image_path: Path) -> None:
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not read image at {image_path}")

    original_height, original_width = image.shape[:2]
    resized_image = cv2.resize(
        image,
        (max(1, original_width // 2), max(1, original_height // 2)),
        interpolation=cv2.INTER_AREA,
    )
    rotated_image = cv2.rotate(resized_image, cv2.ROTATE_180)
    flipped_image = cv2.flip(rotated_image, 0)
    stem = image_path.stem

    results = {
        f"{stem}_01_resized.png": resized_image,
        f"{stem}_02_rotated_180.png": rotated_image,
        f"{stem}_03_flipped_vertically.png": flipped_image,
    }
    for filename, result in results.items():
        output_path = OUTPUT_DIR / filename
        if not cv2.imwrite(str(output_path), result):
            raise IOError(f"Could not save processed image to {output_path}")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    image_paths = sorted(
        path for path in INPUT_DIR.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if len(image_paths) != 5:
        raise ValueError(f"Expected exactly 5 input images in {INPUT_DIR}, found {len(image_paths)}")

    for image_path in image_paths:
        process_image(image_path)
        print(f"Processed {image_path.name}")

    print(f"Saved results to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()