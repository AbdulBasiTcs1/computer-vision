"""Detect visible faces in a real concert-crowd photograph with YuNet."""

from pathlib import Path

import cv2

MODULE_DIR = Path(__file__).resolve().parents[1]
IMAGE_PATH = MODULE_DIR / "assets" / "input" / "crowd.jpg"
MODEL_PATH = MODULE_DIR / "assets" / "models" / "face_detection_yunet_2023mar.onnx"
OUTPUT_PATH = MODULE_DIR / "outputs" / "crowd_faces.png"


def main() -> None:
    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise FileNotFoundError(f"Could not read input image: {IMAGE_PATH}")
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Could not find YuNet model: {MODEL_PATH}")

    height, width = image.shape[:2]
    detector = cv2.FaceDetectorYN.create(
        str(MODEL_PATH),
        "",
        (width, height),
        score_threshold=0.7,
        nms_threshold=0.3,
        top_k=5000,
    )
    _, faces = detector.detect(image)

    result = image.copy()
    face_count = 0 if faces is None else len(faces)
    if faces is not None:
        for face in faces:
            x, y, box_width, box_height = face[:4].astype(int)
            confidence = float(face[-1])
            cv2.rectangle(
                result,
                (x, y),
                (x + box_width, y + box_height),
                (0, 220, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                result,
                f"{confidence:.2f}",
                (x, max(y - 8, 18)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 220, 0),
                2,
                cv2.LINE_AA,
            )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(OUTPUT_PATH), result):
        raise RuntimeError(f"Could not write output image: {OUTPUT_PATH}")
    print(f"Detected {face_count} faces at confidence >= 0.70.")
    print(f"Saved result: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()