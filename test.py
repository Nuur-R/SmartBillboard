import cv2
import threading

video_state = ''  # Variabel global untuk menyimpan state video
state_lock = threading.Lock()  # Lock untuk mengamankan akses ke video_state

def play_video():
    global video_state  # Menggunakan variabel global

    while True:
        with state_lock:
            state = video_state

        if state == 'car':
            video_path='ads/car.mp4'
        elif state == 'motorcycle':
            video_path='ads/motorcycle.mp4'
        else:
            video_path='ads/car.mp4'

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
                break  # Keluar dari loop jika sudah mencapai akhir video

            # Display the resulting frame
            cv2.imshow('Video Player', frame)

            # Add delay to match the video's frame rate
            if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
                break

            # Check for state change
            with state_lock:
                if video_state != state:
                    break

        # Release the capture and close all windows
        cap.release()
        cv2.destroyAllWindows()

def update_state():
    global video_state  # Menggunakan variabel global

    while True:
        state = input("Masukkan state (car/motorcycle) atau 'exit' untuk keluar: ").strip().lower()
        if state == 'exit':
            return
        elif state == 'car' or state == 'motorcycle':
            with state_lock:
                video_state = state
        else:
            print("State tidak valid. Masukkan 'car' atau 'motorcycle'.")

if __name__ == "__main__":
    # Jalankan fungsi di latar belakang dalam sebuah thread
    background_thread = threading.Thread(target=play_video)
    background_thread.daemon = True  # Thread akan berhenti jika program utama berhenti
    background_thread.start()

    # Jalankan fungsi update_state() di thread utama
    update_state()
