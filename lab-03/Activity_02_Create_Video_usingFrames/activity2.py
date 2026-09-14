import os
import cv2


def create_video_from_images(image_folder, output_path, fps=1):
    """
    Reads all images in `image_folder`, sorts them, and writes them
    sequentially into a video file at the given fps.
    """

    # 1. Load Images: collect valid image filenames from the folder
    images = [img for img in os.listdir(image_folder)
              if img.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # IMPORTANT: os.listdir() does not guarantee order — sort explicitly
    # so the video plays image1, image2, image3... in the correct sequence.
    images.sort()

    if not images:
        print("Error: No images found in folder.")
        return

    print(f"Found {len(images)} images: {images}")

    # 2. Read each image using OpenCV, starting with the first
    #    to determine frame width/height for the video.
    first_image_path = os.path.join(image_folder, images[0])
    first_frame = cv2.imread(first_image_path)

    if first_frame is None:
        print(f"Error: Could not read {first_image_path}")
        return

    height, width, channels = first_frame.shape
    print(f"Video frame size set to: {width}x{height}")

    # 3. Create the Video: set up VideoWriter with frame width, height, fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec for .mp4 output
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # 4. Loop through every image, read it, and write it as one video frame
    for image_name in images:
        img_path = os.path.join(image_folder, image_name)
        frame = cv2.imread(img_path)

        if frame is None:
            print(f"Warning: Skipping unreadable file {image_name}")
            continue

        # Guard: resize any image that doesn't match the target dimensions
        if frame.shape[0] != height or frame.shape[1] != width:
            frame = cv2.resize(frame, (width, height))

        video.write(frame)
        print(f"Added frame: {image_name}")

    # 5. Release the writer so the video file is finalized and playable
    video.release()
    print(f"\nVideo successfully saved as: {output_path}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(script_dir, 'images')
    output_path = os.path.join(script_dir, 'output_video.mp4')

    # fps=1 means each image is displayed for 1 second in the final video
    create_video_from_images(image_folder, output_path, fps=1)