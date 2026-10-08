# Tugas Pengolahan Citra Digital

## Tujuan
Membongkar isi sebuah foto menggunakan Python untuk membuktikan bahwa
gambar digital sebenarnya disimpan komputer sebagai data dan angka.

## Foto Contoh
Tiga foto dari perangkat berbeda, untuk menunjukkan bahwa program dapat
membaca foto dari Android, kamera DSLR/mirrorless, dan iPhone.

| File | Perangkat | Format |
|---|---|---|
| `Andro.jpeg` | Android | JPEG |
| `cam.jpeg` | Kamera Sony ILCE-7RM3A | JPEG |
| `coba.heif` | iPhone | HEIF |

Catatan privasi: data lokasi GPS pada foto Android dan iPhone sudah
dihapus sebelum di-upload. Metadata kamera lain tetap ada.

## Cara Menjalankan
1. Install library: `pip install -r requirements.txt
2. Jalankan program: `python main.py` (default membaca `cam.jpeg`)
3. Ganti foto yang dibaca, pilih salah satu:
   - Ubah nilai `NAMA_FILE` di bagian atas `main.py`, atau
   - Jalankan lewat terminal: `python main.py Andro.jpeg`

Foto lain juga bisa dipakai: taruh di folder yang sama, lalu tulis namanya.

## Yang Dianalisis
1. *Metadata foto**: nama file, format, resolusi, tanggal pengambilan,
   kamera, ISO, aperture, focal length
2. **Data gambar**: ukuran, jumlah pixel, nilai pixel, RGB, susunan pixel
3. **Pembuktian gambar = angka**: gambar diubah menjadi array angka
   (NumPy), lalu angkanya diubah dan gambar ikut berubah

## Hasil
Hasil tampil di terminal saat program dijalankan. Bukti visual
(potongan foto asli dan potongan dengan channel hijau diubah menjadi 0)
disimpan otomatis di folder `hasil/`.

## Kesimpulan
Foto addalah susunan angka. Setiap pixel menyimpan tiga nilai (R, G, B)
dengan rentang 0-255. Ketika angka diubah, tampilan gambar ikut berubah.
Metadata EXIF menyimpan informasi kamera dan pengaturan pemotretan dalam
bentuk kode angka yang diterjemahkan menjadi nama tag.