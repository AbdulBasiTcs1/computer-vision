# Lab Task: Play a Video in Reverse Mode using OpenCV

## Files
| File | Purpose |
|---|---|
| `reverse_video.py` | Main script - loads video, plays original + reversed side by side |
| `create_sample_video.py` | Generates the demo `sample_video.mp4` (5 s) |
| `sample_video.mp4` | Test video |
| `output_side_by_side.mp4` | Demo result (left = original, right = reversed) |
| `requirements.txt` | Dependencies |

## Run
```
pip install -r requirements.txt
python create_sample_video.py        # optional, sample already included
python reverse_video.py              # play side by side
python reverse_video.py --video your_video.mp4 --save result.mp4
```
Keys: `SPACE` pause/resume, `q`/`ESC` quit.

## How it works
1. `cv2.VideoCapture` reads all frames into a list.
2. `frames[::-1]` gives the reversed order.
3. Each iteration, frame *i* of the original and frame *i* of the reversed list are
   labelled, joined with `np.hstack`, and shown with `cv2.imshow`.
4. `cv2.waitKey(1000/fps)` keeps playback at the video's real speed (smooth & responsive).
5. Frames are preloaded in memory because seeking backwards in OpenCV is slow/unreliable.
