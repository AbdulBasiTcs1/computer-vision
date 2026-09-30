# Hough Transforms and Face Detection

This lesson introduces two classical Hough-transform tasks and a separate modern face detector. It uses three real photographs, one per task, and writes annotated results to `outputs/`.

## Setup

From this directory, create and activate a virtual environment, then install the lesson dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

On macOS or Linux, activate with `source .venv/bin/activate` and use `python3` instead of `py`.

## Run

```powershell
py examples/01_hough_line_detection.py
py examples/02_hough_circle_detection.py
py examples/03_crowd_face_detection.py
```

The sample photographs and YuNet model are included under `assets/`; no download step is needed. Results are written to `outputs/hough_lines.png`, `outputs/hough_circles.png`, and `outputs/crowd_faces.png`.

## Concepts

- **Lines:** `Canny` extracts edges and `HoughLinesP` finds line segments in the edge map. Threshold, minimum length, and maximum gap control which segments survive.
- **Circles:** `HoughCircles` votes for circle centers and radii. Blur reduces noise; `param2`, radius bounds, and minimum center spacing strongly affect detections.
- **Faces:** YuNet is a learned face detector, not a Hough transform. `FaceDetectorYN` returns face boxes, confidence scores, and landmarks. Faces that are small, turned away, blurred, or occluded may be missed.

These outputs are demonstrations, not measurements or identity recognition. Face detection does not identify people. Get appropriate permission before analyzing or sharing images of people, and do not use this exercise for decisions about individuals.

## Image and model sources

See [ASSETS.md](ASSETS.md) for the exact image URLs, creators, licenses, and model provenance.