# Lab: Feature Extraction with Traditional Approaches
SIFT · SURF · BRIEF · ORB · HOG

## How to run
```bash
pip install -r requirements.txt
python prepare_dataset.py      # builds ./dataset (6 images from scikit-image; or put your own images there)
python feature_extraction.py   # runs everything, writes ./results
```

## What it does
1. **Dataset** – 6 images (astronaut, coffee, cat, rocket, brick texture, text page) in `dataset/`.
2. **Extraction** – SIFT, SURF, BRIEF (FAST detector + BRIEF descriptor), ORB, HOG.
3. **Visualisation** – `results/features_<image>.png` shows the original with keypoints (size/orientation drawn) for each method and the HOG gradient visualisation. `results/matches_*.png` show matches between the original and a rotated (25°), scaled (0.8), noisy copy.
4. **Efficiency** – median of 3 runs: extraction time, keypoints/second, descriptor size.
5. **Accuracy** – ground-truth test: a match is correct if it lands within 3 px of where the known transform says it should. Reported as *matching precision* and *keypoint repeatability*. HOG has no keypoints, so it is tested by classification (sklearn digits, HOG+SVM vs raw pixels+SVM).

## Results (mean over 6 images)
| method                 |   keypoints |   extract_ms |   kp_per_sec |   descriptor_bytes |   precision |   repeatability |
|:-----------------------|------------:|-------------:|-------------:|-------------------:|------------:|----------------:|
| SIFT                   |      654.5  |       121.01 |      5660.22 |                512 |        0.86 |            0.53 |
| SURF (KAZE substitute) |      568    |       277.57 |      2280.94 |                256 |        0.81 |            0.71 |
| BRIEF                  |      559    |         2.6  |    213886    |                 32 |        0.11 |            0.76 |
| ORB                    |      886.17 |         6.65 |    142982    |                 32 |        0.79 |            0.82 |
| HOG                    |      nan    |       145.25 |       nan    |             138384 |      nan    |          nan    |

HOG classification accuracy:

| Unnamed: 0       |   accuracy |
|:-----------------|-----------:|
| Raw pixels + SVM |   0.987037 |
| HOG + SVM        |   0.962963 |

Charts: `results/comparison_charts.png`; raw numbers: `results/all_results.csv`.

## Analysis
| Method | Type | Speed | Robustness | Notes |
|---|---|---|---|---|
| SIFT | float 128-D, scale/rotation invariant | slow (~100+ ms) | very high precision | most reliable; 512-byte descriptor |
| SURF | float 64-D, Hessian + box filters | slow here (KAZE substitute) | good precision, good repeatability | designed to be faster than SIFT; patented |
| BRIEF | binary 256-bit, descriptor only | fastest (~3 ms) | **very low precision** | not rotation/scale invariant, so it fails on the rotated+scaled test; fine for small viewpoint changes |
| ORB | binary 256-bit, oriented FAST + rotated BRIEF | very fast (~6 ms) | good precision, best repeatability | best speed/accuracy trade-off, free to use |
| HOG | dense global gradient histogram | moderate | good for classification/detection | not for keypoint matching; very long vector |

**Conclusion:** SIFT is the most accurate, ORB gives nearly the same quality at ~20x the speed, BRIEF is fastest but lacks rotation/scale invariance, SURF sits between SIFT and ORB, and HOG is the right choice for whole-image / object description (classification, pedestrian detection) rather than point matching.

## Important notes
* **SURF**: it is patented/non-free and is not included in pip builds of OpenCV. The script tries real SURF first; if unavailable (as here) it automatically uses **KAZE**, the closest open-source equivalent, and labels it `SURF (KAZE substitute)`. To use true SURF, build OpenCV with `OPENCV_ENABLE_NONFREE=ON`; no code change is needed.
* Absolute timings depend on your machine; the ranking stays the same.
