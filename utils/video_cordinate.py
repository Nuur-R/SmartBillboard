import cv2
import numpy as np

# List untuk menyimpan titik-titik yang diklik
points = []

# Fungsi untuk menangani klik mouse
def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:  # Ketika tombol kiri mouse ditekan
        points.append((x, y))  # Tambahkan titik ke daftar
        print(f"Koordinat titik yang diklik: X={x}, Y={y}")
        # Gambar titik pada frame
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        # Gambar garis jika ada lebih dari satu titik
        if len(points) > 1:
            cv2.line(frame, points[-2], points[-1], (0, 255, 0), 2)
        cv2.imshow(window_name, frame)

# Open the video file
video_path = "../video/1.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Tidak dapat membuka video {video_path}")
else:
    # Read the first frame from the video
    success, frame = cap.read()

    if success:
        # Mendapatkan dimensi frame
        height, width = frame.shape[:2]
        print(f"Lebar frame: {width}")
        print(f"Tinggi frame: {height}")

        # Menampilkan frame
        window_name = "Sample Frame"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Membuat jendela dengan ukuran yang dapat diubah
        cv2.resizeWindow(window_name, width, height)    # Mengatur ukuran jendela sesuai dengan dimensi frame
        cv2.imshow(window_name, frame)
        cv2.setMouseCallback(window_name, mouse_callback)  # Mengatur callback untuk menangani klik mouse

        # Tunggu hingga tombol 'q' ditekan
        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Menutup jendela
        cv2.destroyAllWindows()

        # Cetak koordinat dalam bentuk yang diminta
        if points:
            print("polygon_points = np.array([")
            for point in points:
                print(f"    [{point[0]}, {point[1]}],")
            print("])")

    else:
        print("Error: Tidak dapat membaca frame dari video.")

    # Release the video capture object
    cap.release()
