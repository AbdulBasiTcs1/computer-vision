"""
Lab Task: Play a Video in Reverse Mode using OpenCV

- Loads a video file
- Reads all frames into memory (so reverse playback is smooth - seeking
  backwards frame by frame with OpenCV is slow and unreliable)
- Plays the ORIGINAL and the REVERSED video side by side
- Optionally saves the side-by-side result to a file

Usage:
    python reverse_video.py                       # uses sample_video.mp4
    python reverse_video.py --video my_clip.mp4
    python reverse_video.py --save comparison.mp4 --no-display

Keys while playing:  q / ESC = quit,  SPACE = pause/resume
"""
import argparse
import sys
import cv2
import numpy as np


def load_frames(path, max_width=640):
    """Read every frame of the video into a list (resized if too wide)."""
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        sys.exit(f"Error: cannot open video '{path}'")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        h, w = frame.shape[:2]
        if w > max_width:                       # keep window a sensible size
            scale = max_width / w
            frame = cv2.resize(frame, (max_width, int(h * scale)))
        frames.append(frame)
    cap.release()

    if not frames:
        sys.exit("Error: video contains no frames")
    return frames, fps


def label(frame, text):
    """Draw a caption on a copy of the frame."""
    f = frame.copy()
    cv2.rectangle(f, (0, 0), (190, 34), (0, 0, 0), -1)
    cv2.putText(f, text, (8, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2, cv2.LINE_AA)
    return f


def main():
    ap = argparse.ArgumentParser(description="Play a video in reverse (side by side)")
    ap.add_argument("--video", default="sample_video.mp4", help="input video path")
    ap.add_argument("--save", default=None, help="save side-by-side result to this file")
    ap.add_argument("--no-display", action="store_true", help="do not open a window")
    args = ap.parse_args()

    frames, fps = load_frames(args.video)
    reversed_frames = frames[::-1]              # the core idea: reverse the frame list
    delay = max(1, int(1000 / fps))             # ms per frame -> real-time speed
    print(f"Loaded {len(frames)} frames @ {fps:.1f} FPS")

    h, w = frames[0].shape[:2]
    writer = None
    if args.save:
        writer = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc(*"mp4v"),
                                 fps, (w * 2, h))

    paused = False
    i = 0
    while i < len(frames):
        left = label(frames[i], "ORIGINAL")
        right = label(reversed_frames[i], "REVERSED")
        combined = np.hstack((left, right))     # side by side

        if writer:
            writer.write(combined)

        if not args.no_display:
            cv2.imshow("Original (left)  vs  Reversed (right)", combined)
            key = cv2.waitKey(delay) & 0xFF
            if key in (ord("q"), 27):
                break
            if key == ord(" "):
                paused = not paused
            while paused:                       # simple pause loop
                key = cv2.waitKey(50) & 0xFF
                if key == ord(" "):
                    paused = False
                elif key in (ord("q"), 27):
                    i = len(frames)
                    break
        i += 1

    if writer:
        writer.release()
        print(f"Saved side-by-side video to {args.save}")
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
