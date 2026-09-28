# OpenCV Foundations

## What is OpenCV?

OpenCV is an open-source library for computer vision and image processing. It provides functions for image and video input/output, transformations, filtering, geometric operations, feature detection, camera calibration, object tracking, and machine-learning inference.

Computer vision is the process of extracting useful information from visual data. A program might answer questions such as: Is this image blurred? Where is the road? Does this frame contain a face? How far away is an object?

## A short history

- OpenCV began at Intel in the late 1990s as a practical, performance-focused computer-vision library.
- It was released as open source so researchers and developers could share algorithms and implementations.
- The project grew through academic, industrial, and community contributions.
- Modern OpenCV supports C++, Python, Java, mobile platforms, and many hardware-accelerated workflows.

Its lasting importance comes from being fast, portable, well documented, and useful both with classical algorithms and with modern neural networks.

## Core terms

- **Pixel**: one sample in an image. A color pixel commonly has blue, green, and red values in OpenCV's default channel order.
- **Image shape**: usually `(height, width, channels)`, for example `(480, 640, 3)`.
- **Frame**: one image from a video stream.
- **Grayscale**: one intensity channel instead of three color channels.
- **ROI**: region of interest, a selected rectangle or mask within an image.
- **Mask**: a binary or weighted image that selects pixels for processing.
- **Threshold**: a rule that separates pixels into groups based on intensity or color.
- **Kernel**: a small matrix used by filters such as blur and edge detection.
- **Contour**: a curve joining boundary points of a connected region.
- **Model inference**: using a trained machine-learning model to produce predictions.

## The basic image pipeline

Most projects can be described as:

1. Capture or load an image.
2. Validate that input exists and has the expected format.
3. Preprocess: resize, crop, denoise, normalize, or change color space.
4. Detect or describe the visual information of interest.
5. Make a decision or measurement.
6. Draw, save, display, or send the result somewhere.
7. Test with varied lighting, viewpoints, devices, and failure cases.

## Why channel order matters

OpenCV reads color images as BGR by default, while many other Python tools use RGB. Convert explicitly when moving data between libraries:

```python
rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
```

## Classical vision and deep learning

Classical operations such as thresholding, contours, morphology, and geometry are transparent and often fast. They work especially well in controlled environments. Deep-learning models can recognize more varied objects but require representative training data, more compute, and careful evaluation. Real systems often combine both approaches.
