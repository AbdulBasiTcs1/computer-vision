"""Lab Task 2: Gaussian blurring and grayscale conversion for five images."""

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

    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)
    output_path = OUTPUT_DIR / f"{image_path.stem}_blurred_grayscale.png"
    if not cv2.imwrite(str(output_path), gray_image):
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