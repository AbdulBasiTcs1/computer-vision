import cv2
from pathlib import Path

# Load the Image
image_path = Path(__file__).resolve().parent / "image.png"
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Couldn't load image at {image_path}")    

# Define rectangle coordinates
start_x, start_y = 50, 50
end_x, end_y = 200, 200

# 1. Draw a rectangle
cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

# 2. Add text label (Blue)
cv2.putText(
    image,
    "Hello, I am Basit!",
    (start_x, start_y - 10),
    cv2.FONT_HERSHEY_COMPLEX,
    1,
    (255, 0, 0),
    2,
)

# Save the output alongside the script
output_path = Path(__file__).resolve().parent / "annotated_image.png"
if not cv2.imwrite(str(output_path), image):
    raise IOError(f"Couldn't save annotated image to {output_path}")

# Show the result
cv2.imshow("Annotated Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()