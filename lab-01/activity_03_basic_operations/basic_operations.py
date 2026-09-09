# Activity 3: Perform Basic Image Operations

import cv2
from pathlib import Path

# Load the Image
image_path = Path(__file__).resolve().parent / "image.png"
image = cv2.imread(str(image_path))

if image is None:
    print(f"Error: could not read image at {image_path}.")
    raise SystemExit(1)

# Step 1: Resize the image
new_width, new_height = 300, 300
resized_image = cv2.resize(image, (new_width, new_height))

# Step 2: Rotate the image 90 degrees clockwise
rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

# Step 3: Flip the image horizontally
flipped_image = cv2.flip(image,1)

# Display all results
cv2.imshow('Original',image)
cv2.imshow('Resized',resized_image)
cv2.imshow('Rotated',rotated_image)
cv2.imshow('Flipped',flipped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()