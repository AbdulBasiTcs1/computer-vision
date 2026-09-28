# Mini Project: Color Object Detector

This small project detects a chosen color in the generated scene. It demonstrates a useful classical-vision pattern: convert to HSV, create a mask, find connected contours, and draw the result.

## Run

From this folder's parent directory:

```powershell
py examples/02_create_sample_image.py
py mini_project/detect_color.py
```

The output is written to `assets/generated/color_detection.png`.

## What to try

- Change `LOWER_HSV` and `UPPER_HSV` to detect the green rectangle.
- Change the minimum contour area.
- Test the detector on a photograph with different lighting.
- Explain why HSV can be more convenient than BGR for color selection.

This is a teaching example, not a production detector. Its fixed thresholds are sensitive to lighting and camera settings.
