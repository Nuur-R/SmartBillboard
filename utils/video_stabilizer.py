from vidstab import VidStab

# Inisialisasi stabilizer
stabilizer = VidStab()

# Path ke video input dan output
input_video = "../video/2.mp4"
output_video = "../video/2s.mp4"

# Membuka input video dan memulai stabilisasi
stabilizer.stabilize(input_path=input_video, output_path=output_video)

print("Video stabilization complete.")
