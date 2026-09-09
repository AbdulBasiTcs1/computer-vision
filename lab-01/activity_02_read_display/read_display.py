# Activity 2: Read and Display Images using OpenCV

import cv2

# Step 1: Read the image from file
image = cv2.imread('image.png')

# Check the image loaded correclty before continuing
if image is None:
    print("Error: could not read image. Check the filename/path.")
    exit()

# Step 2: Display the image
cv2.imshow("Image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

