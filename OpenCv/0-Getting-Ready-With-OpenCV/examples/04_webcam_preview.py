"""Preview a webcam when a desktop camera is available."""

import cv2


def main() -> None:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("No camera is available. Check the connection and permissions.")
        return

    print("Press Q to quit the preview.")
    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read a frame from the camera.")
                break
            cv2.imshow("OpenCV webcam preview", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
