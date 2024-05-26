import cv2

def play_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)  # Convert frame rate to milliseconds

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Display the resulting frame
        cv2.imshow('Video Player', frame)

        # Add delay to match the video's frame rate
        if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
            break

    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'path/to/your/video.mp4'  # Replace with your video path
    play_video(video_path)
