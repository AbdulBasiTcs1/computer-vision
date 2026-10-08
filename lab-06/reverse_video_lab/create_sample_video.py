"""
create_sample_video.py
Generates a short (5 second) demo video 'sample_video.mp4' so the lab task
can be tested without needing any external footage.
A ball bounces across the screen, a frame counter and a progress bar make
the reverse playback easy to see.
"""
import cv2
import numpy as np

WIDTH, HEIGHT, FPS, SECONDS = 640, 360, 30, 5
TOTAL = FPS * SECONDS

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("sample_video.mp4", fourcc, FPS, (WIDTH, HEIGHT))

for i in range(TOTAL):
    t = i / TOTAL
    # animated gradient background
    x = np.linspace(0, 255, WIDTH, dtype=np.uint8)
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    shift = int(t * 255)
    frame[:, :, 0] = (x[None, :] + shift) % 255
    frame[:, :, 1] = 90
    frame[:, :, 2] = 255 - (x[None, :] + shift) % 255
    frame = (frame * 0.5).astype(np.uint8)

    # bouncing ball (moves left -> right, bounces vertically)
    cx = int(50 + t * (WIDTH - 100))
    cy = int(HEIGHT - 60 - abs(np.sin(t * np.pi * 4)) * (HEIGHT - 150))
    cv2.circle(frame, (cx, cy), 32, (0, 220, 255), -1)
    cv2.circle(frame, (cx, cy), 32, (255, 255, 255), 3)

    # frame counter + progress bar
    cv2.putText(frame, f"Frame {i + 1}/{TOTAL}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(frame, (20, HEIGHT - 25), (WIDTH - 20, HEIGHT - 10), (255, 255, 255), 2)
    cv2.rectangle(frame, (20, HEIGHT - 25),
                  (20 + int((WIDTH - 40) * t), HEIGHT - 10), (255, 255, 255), -1)
    out.write(frame)

out.release()
print("Created sample_video.mp4")
