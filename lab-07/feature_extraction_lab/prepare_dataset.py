"""Creates a small test dataset (PNG files) from scikit-image's bundled sample images.
No internet needed. You can also drop your own images into ./dataset instead."""
import os
import numpy as np
from skimage import data
import cv2

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
os.makedirs(OUT, exist_ok=True)

images = {
    "astronaut": data.astronaut(),
    "coffee": data.coffee(),
    "cat": data.chelsea(),
    "rocket": data.rocket(),
    "brick": cv2.cvtColor(data.brick(), cv2.COLOR_GRAY2RGB),
    "text_page": cv2.cvtColor(data.page(), cv2.COLOR_GRAY2RGB),
}
for name, img in images.items():
    img = np.asarray(img)
    if img.ndim == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.path.join(OUT, f"{name}.png"), img)
    print("saved", name, img.shape)
