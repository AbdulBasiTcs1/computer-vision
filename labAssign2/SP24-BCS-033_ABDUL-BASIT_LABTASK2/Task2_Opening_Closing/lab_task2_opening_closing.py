"""
Lab Task 2: Opening and Closing
Name: Abdul Basit | Reg: SP24-BCS-033
Objective: Apply opening and closing and analyze their effects on an image.
"""
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(BASE, "input", "noisy_text.png")
OUT_DIR = os.path.join(BASE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. A different image: binary text image with noise
#    - black specks on the background (salt/"pepper" outside objects)
#    - white holes inside the letters
img = cv2.imread(IN_PATH, cv2.IMREAD_GRAYSCALE)
_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Morphology works on white objects, so invert: text = white, background = black
obj = cv2.bitwise_not(img)

# 2. Structuring elements
k_rect3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
k_ell5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
k_rect9 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))

def op(im, kind, k):
    return cv2.morphologyEx(im, kind, k)

# Opening (erosion -> dilation): removes small white noise outside the text
opening = op(obj, cv2.MORPH_OPEN, k_rect3)
# Closing (dilation -> erosion): fills small holes inside the text
closing = op(obj, cv2.MORPH_CLOSE, k_ell5)
# Opening followed by closing: cleans both kinds of noise
open_close = op(opening, cv2.MORPH_CLOSE, k_ell5)
# Large kernel to show over-processing
open_big = op(obj, cv2.MORPH_OPEN, k_rect9)
close_big = op(obj, cv2.MORPH_CLOSE, k_rect9)

results = {
    "01_original_noisy": obj,
    "02_opening_rect3": opening,
    "03_closing_ellipse5": closing,
    "04_opening_then_closing": open_close,
    "05_opening_rect9_large": open_big,
    "06_closing_rect9_large": close_big,
}
for name, im in results.items():
    # invert back so the saved images are black text on white paper
    cv2.imwrite(os.path.join(OUT_DIR, name + ".png"), cv2.bitwise_not(im))

titles = ["Original (noisy)", "Opening (3x3 rect)", "Closing (5x5 ellipse)",
          "Opening then Closing", "Opening (9x9, too large)", "Closing (9x9, too large)"]
fig, axes = plt.subplots(3, 2, figsize=(12, 10))
for ax, (name, im), t in zip(axes.ravel(), results.items(), titles):
    ax.imshow(cv2.bitwise_not(im), cmap="gray", vmin=0, vmax=255)
    ax.set_title(t)
    ax.axis("off")
fig.suptitle("Opening and Closing on a Noisy Text Image", fontsize=14)
plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "comparison_opening_closing.png"), dpi=110)
plt.close(fig)
print("Done. Results saved in:", OUT_DIR)

"""
DISCUSSION
----------
Opening = erosion followed by dilation.
  * Removes small bright objects/noise specks and thin protrusions outside the
    main shapes, breaks thin bridges, smooths outer contours.
  * Main shapes keep (almost) their original size because the dilation
    restores what the erosion removed.
  * Does NOT fill holes inside letters.

Closing = dilation followed by erosion.
  * Fills small holes/gaps inside objects and joins nearby broken parts,
    smooths contours from the inside.
  * Does NOT remove isolated noise specks (it can even enlarge them).

Opening then closing removes both noise types, giving clean text.

Structuring element: rectangles act stronger on straight edges/corners,
ellipses give smoother, rounder results. Too large a kernel (9x9) damages
the thin strokes of letters (opening erases thin parts, closing merges letters).
Rule of thumb: opening -> denoising background, closing -> repairing objects.
"""
