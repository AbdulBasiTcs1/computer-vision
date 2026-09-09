"""Lab Task 1: Basic Image Operations."""

from pathlib import Path
import cv2


# Load the open-source image included in this submission folder.
submission_dir = Path(__file__).resolve().parent
image_path = submission_dir / "image.png"
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Could not read image at {image_path}")

original_height, original_width = image.shape[:2]

# Resize the image to half its original dimensions.
half_width = max(1, original_width // 2)
half_height = max(1, original_height // 2)
resized_image = cv2.resize(
    image,
    (half_width, half_height),
    interpolation=cv2.INTER_AREA,
)

# Rotate the resized image 180 degrees clockwise.
rotated_image = cv2.rotate(resized_image, cv2.ROTATE_180)

# Flip the rotated image vertically.
flipped_image = cv2.flip(rotated_image, 0)

# Display each stage of the operation.
cv2.imshow("Original Image", image)
cv2.imshow("Resized Image", resized_image)
cv2.imshow("Rotated 180 Degrees", rotated_image)
cv2.imshow("Vertically Flipped Image", flipped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
