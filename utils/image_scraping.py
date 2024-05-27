from bing_image_downloader import downloader

# Mengunduh gambar
def download_bing_images(search_query, num_images=30):
    downloader.download(search_query, limit=num_images,  output_dir='images', adult_filter_off=True, force_replace=False, timeout=60)

# Menjalankan fungsi untuk mengunduh gambar
download_bing_images("mobil ayla di jalan", 30)