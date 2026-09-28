# Getting Ready With OpenCV

OpenCV (Open Source Computer Vision Library) is a set of tools for reading, changing, understanding, and creating images and video. This module assumes basic Python knowledge and prepares you for the later labs in this repository.

## What you will learn

- What computer vision is and what OpenCV provides
- A short history of OpenCV and why it became widely adopted
- How images and video are represented in Python
- How to install OpenCV in an isolated environment
- How to read, create, resize, blur, convert, and save images
- Where computer vision is useful in real products and where it needs care

## Quick start

From the repository root on Windows PowerShell:

```powershell
cd 'OpenCv/0-Getting-Ready-With-OpenCV'
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py examples/01_check_installation.py
py examples/02_create_sample_image.py
py examples/03_image_basics.py
```

On macOS or Linux, activate with `source .venv/bin/activate` and use `python3` instead of `py`.

The examples write generated files into `assets/generated/`, which is created automatically. GUI windows may not work in remote or headless environments; `03_image_basics.py` saves its result so it can still be inspected.

## Suggested order

1. Read [OPENCV_FOUNDATIONS.md](OPENCV_FOUNDATIONS.md).
2. Complete [SETUP.md](SETUP.md).
3. Run the scripts in `examples/` in numerical order.
4. Read [REAL_WORLD_USE_CASES.md](REAL_WORLD_USE_CASES.md).
5. Try the [mini project](mini_project/README.md).
6. Use [EXERCISES.md](EXERCISES.md) to check your understanding.
7. Continue with [LEARNING_PATH.md](LEARNING_PATH.md).

## Important idea

OpenCV is a toolkit, not a complete artificial-intelligence model. Traditional image processing, camera geometry, feature extraction, tracking, and deep-learning inference can all be built around it. A useful computer-vision system also needs good data, testing, performance checks, and responsible handling of people and their images.
