import cv2
import threading

# Global variable to keep track of the current video file
current_video = 'video/iklan/1.mp4'
play_video = True

def video_player():
    global play_video, current_video
    while True:
        # Open the video file
        cap = cv2.VideoCapture(current_video)
        
        if not cap.isOpened():
            print(f"Error opening video file {current_video}")
            return
        
        while play_video and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video Playback', frame)
            
            # Wait for 25ms before moving to next frame
            # This is to simulate 40fps (25ms/frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                play_video = False
                break

        cap.release()
        cv2.destroyAllWindows()

def command_listener():
    global current_video, play_video
    while True:
        cmd = input("Enter new video number: ")
        new_video = f"video/iklan/{cmd}.mp4"
        play_video = False
        current_video = new_video
        play_video = True

if __name__ == "__main__":
    # Create and start the video player thread
    video_thread = threading.Thread(target=video_player)
    video_thread.start()
    
    # Start the command listener in the main thread
    command_listener()
