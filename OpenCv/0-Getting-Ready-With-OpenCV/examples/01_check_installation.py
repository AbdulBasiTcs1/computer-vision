"""Confirm that the local OpenCV environment is ready."""

import cv2
import numpy as np

print("OpenCV is ready")
print(f"OpenCV version: {cv2.__version__}")
print(f"NumPy version: {np.__version__}")
