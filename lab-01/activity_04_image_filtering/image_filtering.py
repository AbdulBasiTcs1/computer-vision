# Activity 4: Apply Image Filtering Techniques

import cv2
from pathlib import Path

# Load the Image
image_path = Path(__file__).resolve().parent / "image.png"
image = cv2.imread(str(image_path))

if image is None:
    print("Error: could not read image. Check the filename/path.")
    exit()

# Step 1: Apply Gauusian Blur
kernel_size = 5
blurred_image = cv2.GaussianBlur(image,(kernel_size,kernel_size),0)

# Step 2: Convert to Grayscale
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

cv2.imshow('Original', image)
cv2.imshow('Blurred', blurred_image)
cv2.imshow('Grayscale', gray_image)

cv2.waitKey(0)
cv2.destroyAllWindows()