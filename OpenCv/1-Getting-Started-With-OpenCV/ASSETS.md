# Image and Model Credits

Only the three sample photographs needed by this lesson are included. The images are not training data and are not used to identify anyone.

| Local file | Use | Source and creator | License |
| --- | --- | --- | --- |
| `assets/input/building.jpg` | Hough line detection | [OpenCV samples: building.jpg](https://github.com/opencv/opencv/blob/4.x/samples/data/building.jpg) | OpenCV repository license: [Apache-2.0](https://github.com/opencv/opencv/blob/4.x/LICENSE) |
| `assets/input/smarties.png` | Hough circle detection | [OpenCV samples: smarties.png](https://github.com/opencv/opencv/blob/4.x/samples/data/smarties.png) | OpenCV repository license: [Apache-2.0](https://github.com/opencv/opencv/blob/4.x/LICENSE) |
| `assets/input/crowd.jpg` | Crowd face detection | [A crowd of people standing around each other](https://unsplash.com/photos/a-crowd-of-people-standing-around-each-other-E2udo40OrWY), by [Tijs van Leur](https://unsplash.com/@tijsvl) | [Unsplash License](https://unsplash.com/license) |

## Face detector model

`assets/models/face_detection_yunet_2023mar.onnx` is the YuNet face detector from the [OpenCV Zoo](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet). Its model card and license are maintained in that directory. The example uses OpenCV's `FaceDetectorYN` API and has been checked with OpenCV 5.

The included crowd image shows a concert audience. At the example's default confidence threshold, YuNet detects some, not all, visible faces; the count is not a crowd-size estimate. Detection results depend on image quality, face size, pose, lighting, and model version.