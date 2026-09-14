import os
import cv2


# Play a video file located in the same folder as this script.
def play_video(video_path):
    # Open the video capture object.
    cap = cv2.VideoCapture(video_path)

    # Check whether the video file opened successfully.
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    # Read and display frames until the video ends or the user presses 'q'.
    while True:
        ret, frame = cap.read()

        # Stop if no frame is available (end of video).
        if not ret:
            print("End of video.")
            break

        # Show the current frame in a window.
        cv2.imshow('Video Playback', frame)

        # Press 'q' to quit the playback.
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release resources after playback ends.
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(script_dir, 'random_video.mp4')
    play_video(video_path)