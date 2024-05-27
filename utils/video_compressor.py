import ffmpeg

def compress_video(input_file, output_file, target_bitrate='1M'):
    """
    Mengompresi video menggunakan ffmpeg.

    Args:
        input_file (str): Path ke file video input.
        output_file (str): Path ke file video output yang dikompresi.
        target_bitrate (str): Target bitrate untuk kompresi (default: '1M' untuk 1 Mbps).
    """
    try:
        ffmpeg.input(input_file).output(output_file, video_bitrate=target_bitrate).run(overwrite_output=True)
        print(f"Video berhasil dikompresi dan disimpan di {output_file}")
    except ffmpeg.Error as e:
        print(f"Terjadi kesalahan saat mengompresi video: {e.stderr.decode()}")

if __name__ == "__main__":
    input_video_path = '../video/20240524_084746.mp4'  # Ganti dengan path video input Anda
    output_video_path = '../video/3.mp4'  # Ganti dengan path video output yang diinginkan
    compress_video(input_video_path, output_video_path)
