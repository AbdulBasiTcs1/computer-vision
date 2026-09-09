# Activity 2: Read and Display Images using OpenCV

import cv2
from pathlib import Path

# Step 1: Read the image from file
image_path = Path(__file__).resolve().parent / "image.png"
image = cv2.imread(str(image_path))

# Check if the image loaded correctly before continuing
if image is None:
    print(f"Error: could not read image at {image_path}.")
    raise SystemExit(1)

# Step 2: Display the image
cv2.imshow("Image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

