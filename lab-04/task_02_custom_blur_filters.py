import argparse
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
IMAGE_PATH = ROOT / "lab-01" / "activity_04_image_filtering" / "image.png"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def apply_convolution(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    pad_h = kernel.shape[0] // 2
    pad_w = kernel.shape[1] // 2
    padded = cv2.copyMakeBorder(
        image,
        pad_h,
        pad_h,
        pad_w,
        pad_w,
        cv2.BORDER_REFLECT,
    )

    result = np.zeros_like(image, dtype=np.float32)
    for r in range(image.shape[0]):
        for c in range(image.shape[1]):
            window = padded[r : r + kernel.shape[0], c : c + kernel.shape[1]]
            result[r, c] = np.sum(window * kernel)

    return np.clip(result, 0, 255).astype(np.uint8)


def save_or_show(window_name: str, image: np.ndarray, filename: str, show: bool) -> None:
    cv2.imwrite(str(OUTPUT_DIR / filename), image)
    if show:
        cv2.imshow(window_name, image)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply custom blur kernels and compare with OpenCV blur techniques.")
    parser.add_argument("--show", action="store_true", help="Display the generated images in windows after saving them.")
    args = parser.parse_args()

    image = cv2.imread(str(IMAGE_PATH), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    box_blur = cv2.blur(gray, (5, 5))
    gaussian_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    median_blur = cv2.medianBlur(gray, 5)

    average_3x3 = np.ones((3, 3), dtype=np.float32) / 9.0
    average_5x5 = np.ones((5, 5), dtype=np.float32) / 25.0

    x = np.arange(-2, 3, dtype=np.float32)
    y = np.arange(-2, 3, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    custom_gaussian = np.exp(-(xx**2 + yy**2) / 2.5)
    custom_gaussian /= custom_gaussian.sum()

    motion_kernel = np.zeros((9, 9), dtype=np.float32)
    motion_kernel[4, :] = 1 / 9.0

    custom_box_3 = apply_convolution(gray, average_3x3)
    custom_box_5 = apply_convolution(gray, average_5x5)
    custom_gaussian_filter = apply_convolution(gray, custom_gaussian)
    custom_motion_blur = apply_convolution(gray, motion_kernel)

    save_or_show("Original Gray", gray, "01_original_gray.png", args.show)
    save_or_show("OpenCV Box Blur", box_blur, "02_opencv_box_blur.png", args.show)
    save_or_show("OpenCV Gaussian", gaussian_blur, "03_opencv_gaussian_blur.png", args.show)
    save_or_show("OpenCV Median", median_blur, "04_opencv_median_blur.png", args.show)
    save_or_show("Custom 3x3 Average", custom_box_3, "05_custom_average_3x3.png", args.show)
    save_or_show("Custom 5x5 Average", custom_box_5, "06_custom_average_5x5.png", args.show)
    save_or_show("Custom Gaussian Kernel", custom_gaussian_filter, "07_custom_gaussian_kernel.png", args.show)
    save_or_show("Custom Motion Blur", custom_motion_blur, "08_custom_motion_blur.png", args.show)

    print("Custom blur results saved in:", OUTPUT_DIR)
    print("Comparison summary:")
    print("- 3x3 average kernel: light smoothing")
    print("- 5x5 average kernel: stronger smoothing and reduced detail")
    print("- Gaussian kernel: smoother, more natural blur")
    print("- Motion blur: directional smoothing along one axis")
    print("- OpenCV blur, GaussianBlur, and medianBlur provide standard reference methods")

    if args.show:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
