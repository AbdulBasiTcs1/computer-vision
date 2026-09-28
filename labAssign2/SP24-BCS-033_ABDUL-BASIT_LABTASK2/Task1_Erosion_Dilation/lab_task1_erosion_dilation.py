"""
Lab Task 1: Erosion and Dilation
Name: Abdul Basit | Reg: SP24-BCS-033
Objective: Implement and understand erosion and dilation using OpenCV.
"""
import os
import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
IN_PATH = os.path.join(BASE, "input", "coins.png")
OUT_DIR = os.path.join(BASE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Choose an image for testing (grayscale, then Otsu threshold -> binary)
gray = cv2.imread(IN_PATH, cv2.IMREAD_GRAYSCALE)
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite(os.path.join(OUT_DIR, "00_original_gray.png"), gray)
cv2.imwrite(os.path.join(OUT_DIR, "00_original_binary.png"), binary)

# 2. Erosion / dilation with varying kernel sizes and iterations
kernel_sizes = [3, 7, 11]      # varying kernel size (iterations fixed = 1)
iteration_values = [1, 3, 5]   # varying iterations (kernel fixed = 5x5)

def erode(img, k, it):
    return cv2.erode(img, np.ones((k, k), np.uint8), iterations=it)

def dilate(img, k, it):
    return cv2.dilate(img, np.ones((k, k), np.uint8), iterations=it)

def save(name, img):
    cv2.imwrite(os.path.join(OUT_DIR, name), img)

def show_grid(title, items, fname, cols=4):
    rows = int(np.ceil(len(items) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    for ax in np.array(axes).ravel():
        ax.axis("off")
    for ax, (label, im) in zip(np.array(axes).ravel(), items):
        ax.imshow(im, cmap="gray", vmin=0, vmax=255)
        ax.set_title(label, fontsize=10)
    fig.suptitle(title, fontsize=14)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, fname), dpi=110)
    plt.close(fig)

# --- A) Effect of kernel size (iterations = 1)
items = [("Original (binary)", binary)]
for k in kernel_sizes:
    e, d = erode(binary, k, 1), dilate(binary, k, 1)
    save(f"erosion_k{k}_it1.png", e)
    save(f"dilation_k{k}_it1.png", d)
    items += [(f"Erosion k={k}, it=1", e), (f"Dilation k={k}, it=1", d)]
show_grid("Effect of Kernel Size (iterations = 1)", items,
          "comparison_kernel_sizes.png", cols=4 if False else 3)

# --- B) Effect of iterations (kernel = 5x5)
items = [("Original (binary)", binary)]
for it in iteration_values:
    e, d = erode(binary, 5, it), dilate(binary, 5, it)
    save(f"erosion_k5_it{it}.png", e)
    save(f"dilation_k5_it{it}.png", d)
    items += [(f"Erosion k=5, it={it}", e), (f"Dilation k=5, it={it}", d)]
show_grid("Effect of Iterations (kernel = 5x5)", items,
          "comparison_iterations.png", cols=3)

# --- C) Also apply on the grayscale image (intensity min/max filter)
g_items = [("Original (gray)", gray),
           ("Erosion (gray) k=5", erode(gray, 5, 1)),
           ("Dilation (gray) k=5", dilate(gray, 5, 1))]
save("gray_erosion_k5_it1.png", g_items[1][1])
save("gray_dilation_k5_it1.png", g_items[2][1])
show_grid("Grayscale Erosion and Dilation", g_items, "comparison_grayscale.png", cols=3)

print("Done. Results saved in:", OUT_DIR)

"""
EXPLANATION
-----------
Erosion  : a pixel stays white only if ALL pixels under the kernel are white.
           White regions shrink, small white noise/objects vanish, objects
           separate (thin connections break).
Dilation : a pixel becomes white if ANY pixel under the kernel is white.
           White regions grow, small black holes/gaps close, objects merge.

Kernel size : bigger kernel = stronger effect per pass. With k=3 the coin
              edges move ~1 px; with k=11 they move ~5 px, small details vanish
              quickly and neighbouring coins start to merge (dilation) or
              shrink to small blobs (erosion).
Iterations  : repeating the operation n times with a k x k kernel is roughly
              like one operation with a larger kernel (effective size ~ n*(k-1)+1)
              but with a more controlled/gradual result. More iterations = more
              shrinkage (erosion) or growth (dilation).
Trade-off   : too small -> little visible change; too large -> loss of shape
              and detail (objects disappear or merge).
"""
