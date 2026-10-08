"""
Feature Extraction with Traditional Approaches
SIFT | SURF | BRIEF | ORB | HOG

For every image in ./dataset this script:
  1. extracts features with each method,
  2. saves a figure with the original image + keypoints (and the HOG visualisation),
  3. measures computational efficiency (time, keypoints/sec, descriptor size),
  4. measures accuracy (matching against a KNOWN geometric transform),
  5. writes CSV tables and comparison charts to ./results.

Accuracy protocol: each image is rotated, scaled and slightly noised using a known
homography H. Features are matched between original and transformed image (Lowe ratio
test / Hamming or L2 distance). A match is CORRECT if the matched keypoint lands within
3 px of where H says it should be. Precision = correct matches / all matches.
Repeatability = keypoints of the original that re-appear in the transformed image.
HOG is a dense, global descriptor (no keypoints) so it is evaluated separately:
a small image-classification test (digits dataset, HOG + SVM vs raw pixels + SVM).

Notes
  * SURF is patented/non-free and is missing from standard pip OpenCV builds.
    The script tries real SURF first; if unavailable it falls back to KAZE
    (the closest open-source Hessian-based, float-descriptor detector) and labels it.
  * BRIEF is only a descriptor, so it is paired with the FAST detector (CenSurE/STAR in
    OpenCV-contrib is also possible). Uses OpenCV-contrib BRIEF, falling back to skimage.
"""
import os, glob, time
import numpy as np
import pandas as pd
import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from skimage.feature import hog, BRIEF
from skimage import exposure

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "dataset")
RES = os.path.join(BASE, "results")
os.makedirs(RES, exist_ok=True)
N_REPEAT = 3          # timing repetitions (median is reported)
MAX_KP = 1000         # cap keypoints for fairness
PX_TOL = 3.0          # pixel tolerance for a "correct" match


# ----------------------------------------------------------------- extractors
def make_surf():
    try:
        s = cv2.xfeatures2d.SURF_create(hessianThreshold=400)
        return "SURF", s, False
    except Exception:
        k = cv2.KAZE_create()
        return "SURF (KAZE substitute)", k, True


def extract_sift(gray):
    s = cv2.SIFT_create(nfeatures=MAX_KP)
    return s.detectAndCompute(gray, None)


def extract_surf(gray):
    name, s, _ = make_surf()
    kp, des = s.detectAndCompute(gray, None)
    if len(kp) > MAX_KP:
        idx = np.argsort([-k.response for k in kp])[:MAX_KP]
        kp = [kp[i] for i in idx]; des = des[idx]
    return kp, des


def extract_orb(gray):
    o = cv2.ORB_create(nfeatures=MAX_KP)
    return o.detectAndCompute(gray, None)


def extract_brief(gray):
    """FAST detector + BRIEF descriptor."""
    fast = cv2.FastFeatureDetector_create(threshold=25)
    kp = fast.detect(gray, None)
    kp = sorted(kp, key=lambda k: -k.response)[:MAX_KP]
    try:
        br = cv2.xfeatures2d.BriefDescriptorExtractor_create(32)
        kp, des = br.compute(gray, kp)
    except Exception:  # skimage fallback -> pack to bytes for Hamming matching
        pts = np.array([k.pt[::-1] for k in kp])
        ext = BRIEF(descriptor_size=256, patch_size=49)
        ext.extract(gray, pts)
        kp = [kp[i] for i in np.where(ext.mask)[0]]
        des = np.packbits(ext.descriptors.astype(np.uint8), axis=1)
    return kp, des


SURF_NAME = make_surf()[0]
METHODS = {   # name: (function, norm for matcher)
    "SIFT": (extract_sift, cv2.NORM_L2),
    SURF_NAME: (extract_surf, cv2.NORM_L2),
    "BRIEF": (extract_brief, cv2.NORM_HAMMING),
    "ORB": (extract_orb, cv2.NORM_HAMMING),
}


def extract_hog(gray, size=(256, 256)):
    g = cv2.resize(gray, size)
    return hog(g, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
               block_norm="L2-Hys", visualize=True)


# ----------------------------------------------------------------- helpers
def load_images():
    files = sorted(glob.glob(os.path.join(DATA, "*.*")))
    out = []
    for f in files:
        img = cv2.imread(f)
        if img is None:
            continue
        h, w = img.shape[:2]
        if max(h, w) > 600:                      # keep it fast
            s = 600 / max(h, w)
            img = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        out.append((os.path.splitext(os.path.basename(f))[0], img))
    return out


def transform_image(img, angle=25, scale=0.8, noise=6, seed=0):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
    warped = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    rng = np.random.default_rng(seed)
    warped = np.clip(warped.astype(np.float32) + rng.normal(0, noise, warped.shape), 0, 255).astype(np.uint8)
    H = np.vstack([M, [0, 0, 1]])
    return warped, H


def timed(fn, *a):
    ts, res = [], None
    for _ in range(N_REPEAT):
        t = time.perf_counter(); res = fn(*a); ts.append(time.perf_counter() - t)
    return res, float(np.median(ts))


def match_and_score(kp1, des1, kp2, des2, norm, H):
    if des1 is None or des2 is None or len(kp1) < 2 or len(kp2) < 2:
        return 0, 0, 0.0, 0.0
    bf = cv2.BFMatcher(norm)
    t = time.perf_counter()
    knn = bf.knnMatch(des1, des2, k=2)
    match_time = time.perf_counter() - t
    good = [m[0] for m in knn if len(m) == 2 and m[0].distance < 0.8 * m[1].distance]
    if not good:
        return 0, 0, 0.0, match_time
    p1 = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    p2 = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    proj = cv2.perspectiveTransform(p1, H)
    err = np.linalg.norm(proj - p2, axis=2).ravel()
    correct = int((err < PX_TOL).sum())
    return len(good), correct, correct / len(good), match_time


def repeatability(kp1, kp2, H):
    if not kp1 or not kp2:
        return 0.0
    p1 = np.float32([k.pt for k in kp1]).reshape(-1, 1, 2)
    p1w = cv2.perspectiveTransform(p1, H).reshape(-1, 2)
    p2 = np.float32([k.pt for k in kp2])
    d = np.linalg.norm(p1w[:, None, :] - p2[None, :, :], axis=2).min(axis=1)
    h, w = 1e9, 1e9
    return float((d < PX_TOL).mean())


# ----------------------------------------------------------------- main
def main():
    images = load_images()
    if not images:
        raise SystemExit("No images in ./dataset - run prepare_dataset.py first.")
    rows = []
    for name, img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        warped, H = transform_image(img)
        gray_w = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

        fig, axes = plt.subplots(1, 6, figsize=(26, 5.4))
        axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)); axes[0].set_title(f"Original: {name}")

        for ax, (mname, (fn, norm)) in zip(axes[1:5], METHODS.items()):
            (kp, des), t_ext = timed(fn, gray)
            (kp2, des2) = fn(gray_w)
            n_good, n_correct, prec, t_match = match_and_score(kp, des, kp2, des2, norm, H)
            rep = repeatability(kp, kp2, H)
            vis = cv2.drawKeypoints(img, kp, None, color=(0, 255, 0),
                                    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            ax.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
            ax.set_title(f"{mname}\n{len(kp)} keypoints, {t_ext*1000:.1f} ms")
            dsize = (des.shape[1] * des.dtype.itemsize) if des is not None and len(des) else 0
            rows.append(dict(image=name, method=mname, keypoints=len(kp),
                             extract_ms=t_ext * 1000,
                             kp_per_sec=len(kp) / t_ext if t_ext else 0,
                             descriptor_bytes=dsize, matches=n_good, correct=n_correct,
                             precision=prec, repeatability=rep, match_ms=t_match * 1000))
            # side-by-side match figure
            if des is not None and des2 is not None and len(kp) > 1 and len(kp2) > 1:
                bf = cv2.BFMatcher(norm)
                knn = bf.knnMatch(des, des2, k=2)
                good = [m[0] for m in knn if len(m) == 2 and m[0].distance < 0.8 * m[1].distance]
                good = sorted(good, key=lambda m: m.distance)[:40]
                mv = cv2.drawMatches(img, kp, warped, kp2, good, None,
                                     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                cv2.imwrite(os.path.join(RES, f"matches_{name}_{mname.split()[0]}.png"), mv)

        # HOG
        (fd, hog_img), t_hog = timed(extract_hog, gray)
        hog_img = exposure.rescale_intensity(hog_img, in_range=(0, hog_img.max() + 1e-9))
        axes[5].imshow(hog_img, cmap="gray")
        axes[5].set_title(f"HOG\nvector length {len(fd)}, {t_hog*1000:.1f} ms")
        rows.append(dict(image=name, method="HOG", keypoints=np.nan, extract_ms=t_hog * 1000,
                         kp_per_sec=np.nan, descriptor_bytes=len(fd) * 4, matches=np.nan,
                         correct=np.nan, precision=np.nan, repeatability=np.nan, match_ms=np.nan))
        for a in axes: a.axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(RES, f"features_{name}.png"), dpi=110, bbox_inches="tight", pad_inches=0.2)
        plt.close()
        print("done", name)

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RES, "all_results.csv"), index=False)
    summ = df.groupby("method").agg(
        keypoints=("keypoints", "mean"), extract_ms=("extract_ms", "mean"),
        kp_per_sec=("kp_per_sec", "mean"), descriptor_bytes=("descriptor_bytes", "mean"),
        precision=("precision", "mean"), repeatability=("repeatability", "mean")).round(3)
    order = ["SIFT", SURF_NAME, "BRIEF", "ORB", "HOG"]
    summ = summ.loc[[m for m in order if m in summ.index]]

    # ---- HOG classification test (accuracy for the dense descriptor)
    from sklearn import datasets, svm
    from sklearn.model_selection import train_test_split
    digits = datasets.load_digits()
    X_raw = digits.images
    t = time.perf_counter()
    X_hog = np.array([hog(im, orientations=9, pixels_per_cell=(2, 2), cells_per_block=(2, 2)) for im in X_raw])
    hog_time = time.perf_counter() - t
    res = {}
    for label, X in [("Raw pixels + SVM", X_raw.reshape(len(X_raw), -1)), ("HOG + SVM", X_hog)]:
        Xtr, Xte, ytr, yte = train_test_split(X, digits.target, test_size=0.3, random_state=0, stratify=digits.target)
        res[label] = svm.SVC(kernel="rbf", gamma="scale").fit(Xtr, ytr).score(Xte, yte)
    pd.Series(res, name="accuracy").to_csv(os.path.join(RES, "hog_classification_accuracy.csv"))
    summ.to_csv(os.path.join(RES, "summary_comparison.csv"))

    # ---- charts
    fig, ax = plt.subplots(1, 3, figsize=(17, 4.5))
    summ["extract_ms"].plot.bar(ax=ax[0], color="#4C72B0"); ax[0].set_title("Extraction time (ms, lower = faster)")
    summ["precision"].dropna().plot.bar(ax=ax[1], color="#55A868"); ax[1].set_title("Matching precision under rotation+scale+noise")
    summ["repeatability"].dropna().plot.bar(ax=ax[2], color="#C44E52"); ax[2].set_title("Keypoint repeatability")
    for a in ax: a.tick_params(axis="x", rotation=30); a.set_xlabel("")
    plt.tight_layout(); plt.savefig(os.path.join(RES, "comparison_charts.png"), dpi=120); plt.close()

    print("\n=== SUMMARY (mean over all images) ===")
    print(summ.to_string())
    print("\n=== HOG classification (sklearn digits) ===")
    for k, v in res.items(): print(f"{k}: {v*100:.2f}%")
    print(f"(HOG extraction for {len(X_raw)} digit images took {hog_time:.2f}s)")
    print(f"\nResults saved in: {RES}")


if __name__ == "__main__":
    main()
