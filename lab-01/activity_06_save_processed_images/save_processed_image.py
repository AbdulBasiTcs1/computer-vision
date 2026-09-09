# Activity 6: Save Processed Images to the Local Filesystem

import cv2
from pathlib import Path

activity_dir = Path(__file__).resolve().parent
image_path = activity_dir / "image.png"
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Couldn't load image at {image_path}")

# Process the image before saving it.
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

output_path = activity_dir / "output_image.jpg"
if not cv2.imwrite(str(output_path), gray_image):
    raise IOError(f"Couldn't save processed image to {output_path}")

print(f"Processed image saved to {output_path}")
