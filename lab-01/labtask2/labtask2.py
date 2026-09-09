"""Lab Task 2: Image Filtering Techniques."""

from pathlib import Path
import cv2


submission_dir = Path(__file__).resolve().parent
image_path = submission_dir / "image.png"
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Could not read image at {image_path}")

# Blur the image with a 5x5 Gaussian kernel.
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

# Convert the blurred image to grayscale.
gray_image = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2GRAY)

# Save the processed image in this submission folder.
output_path = submission_dir / "blurred_grayscale_image.png"
if not cv2.imwrite(str(output_path), gray_image):
    raise IOError(f"Could not save processed image to {output_path}")

print(f"Processed image saved to {output_path}")

# Display each stage of the operation.
cv2.imshow("Original Image", image)
cv2.imshow("Gaussian Blurred Image", blurred_image)
cv2.imshow("Grayscale Image", gray_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
