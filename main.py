import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from pillow_heif import register_heif_opener
import numpy as np

register_heif_opener()

# ==========================================
# PENGATURAN: GANTI NAMA FILE DI SINI
# ==========================================
# Foto contoh yang tersedia:
#   "Andro.jpeg" -> foto dari Android
#   "cam.jpeg"   -> foto dari kamera DSLR/mirrorless (Sony)
#   "coba.heif"  -> foto dari iPhone
# Foto lain juga bisa dipakai: taruh di folder ini, lalu tulis namanya.

NAMA_FILE = "cam.jpeg"

# Cara lain: pilih foto lewat terminal tanpa mengubah kode
#   python main.py Andro.jpeg
if len(sys.argv) > 1:
    NAMA_FILE = sys.argv[1]

# Cek apakah file ada
if not os.path.exists(NAMA_FILE):
    print(f"File '{NAMA_FILE}' tidak ditemukan.")
    print("Foto yang tersedia di folder ini:")
    for f in sorted(os.listdir(".")):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".heic", ".heif")):
            print(" -", f)
    sys.exit()


# ==========================================
# 1. MEMBUKA FOTO
# ==========================================

foto = Image.open(NAMA_FILE)


# ==========================================
# 2. INFORMASI DASAR FOTO
# ==========================================

print("=== INFORMASI FOTO ===")

# Mengambil lebar dan tinggi gambar
lebar, tinggi = foto.size

# Menghitung jumlah pixel
jumlah_pixel = lebar * tinggi

print("Nama file      :", os.path.basename(NAMA_FILE))
print("Format         :", foto.format)
print("Ukuran         :", foto.size)
print("Mode warna     :", foto.mode)
print("Lebar          :", lebar, "pixel")
print("Tinggi         :", tinggi, "pixel")
print("Jumlah pixel   :", jumlah_pixel)
print("Resolusi       :", lebar, "x", tinggi, "pixel")
print("DPI            :", foto.info.get("dpi", "Tidak tersedia"))


# ==========================================
# 3. METADATA / EXIF (TAG PILIHAN)
# ==========================================

print("\n=== METADATA FOTO ===")

# Membaca EXIF utama
exif_data = foto.getexif()

# Membaca Exif IFD (tempat ISO, aperture, focal length, dll)
try:
    exif_detail = exif_data.get_ifd(0x8769)
except Exception:
    exif_detail = {}

# Gabungkan semua tag ke satu dictionary
# (kode angka diterjemahkan menjadi nama teks lewat TAGS)
semua_exif = {}

for kode, nilai in exif_data.items():
    semua_exif[TAGS.get(kode, kode)] = nilai

for kode, nilai in exif_detail.items():
    semua_exif[TAGS.get(kode, kode)] = nilai

# Hanya tampilkan tag yang penting
tag_pilihan = [
    "Make",
    "Model",
    "DateTimeOriginal",
    "ExposureTime",
    "FNumber",
    "ISOSpeedRatings",
    "FocalLength",
    "ExifImageWidth",
    "ExifImageHeight"
]

ada_tag = False

for nama_tag in tag_pilihan:
    if nama_tag in semua_exif:
        print(nama_tag, ":", semua_exif[nama_tag])
        ada_tag = True

if not ada_tag:
    print("Metadata EXIF tidak tersedia.")


# ==========================================
# 4. INFORMASI KAMERA
# ==========================================

print("\n=== INFORMASI KAMERA ===")

# Tiap item: (label, [kemungkinan nama tag])
metadata_dicari = [
    ("Merek Kamera",        ["Make"]),
    ("Model Kamera",        ["Model"]),
    ("Tanggal Pengambilan", ["DateTimeOriginal", "DateTime"]),
    ("ISO",                 ["ISOSpeedRatings", "PhotographicSensitivity", "ISO"]),
    ("Aperture",            ["FNumber"]),
    ("Focal Length",        ["FocalLength"]),
]

for label, daftar_tag in metadata_dicari:

    nilai = None

    for tag in daftar_tag:
        if tag in semua_exif:
            nilai = semua_exif[tag]
            break

    # Beberapa perangkat menyimpan ISO sebagai tuple, ambil nilai pertama
    if isinstance(nilai, (tuple, list)) and len(nilai) > 0:
        nilai = nilai[0]

    if nilai is None:
        print(label, ": Tidak tersedia")
    elif label == "Aperture":
        print(label, f": f/{float(nilai)}")
    elif label == "Focal Length":
        print(label, f": {float(nilai)} mm")
    else:
        print(label, ":", nilai)


# ==========================================
# 5. NILAI PIXEL
# ==========================================

print("\n=== NILAI PIXEL ===")

koordinat = [
    (0, 0),
    (10, 10),
    (100, 100)
]

for x, y in koordinat:

    if x < lebar and y < tinggi:

        nilai_pixel = foto.getpixel((x, y))

        print(f"Pixel ({x},{y}) :", nilai_pixel)


# ==========================================
# 6. DATA RGB
# ==========================================

print("\n=== DATA RGB PIXEL (0,0) ===")

pixel = foto.getpixel((0, 0))

if foto.mode in ("RGB", "RGBA"):

    r, g, b = pixel[:3]

    print("Nilai R (Red)   :", r)
    print("Nilai G (Green) :", g)
    print("Nilai B (Blue)  :", b)

else:

    print("Foto bukan dalam mode RGB.")


# ==========================================
# 7. SUSUNAN PIXEL
# ==========================================

print("\n=== CONTOH SUSUNAN PIXEL ===")

print("Menampilkan 3 baris x 5 kolom pertama:")

for y in range(3):

    baris = []

    for x in range(5):

        pixel = foto.getpixel((x, y))

        baris.append(pixel)

    print(baris)


# ==========================================
# 8. GAMBAR SEBAGAI ARRAY ANGKA
# ==========================================

print("\n=== GAMBAR SEBAGAI ARRAY ANGKA ===")

# Mengubah seluruh gambar menjadi array angka
array_foto = np.array(foto.convert("RGB"))

print("Bentuk array   :", array_foto.shape)   # (tinggi, lebar, 3)
print("Tipe data      :", array_foto.dtype)   # uint8 = angka 0-255
print("Nilai minimum  :", array_foto.min())
print("Nilai maksimum :", array_foto.max())
print("Total angka    :", array_foto.size)    # tinggi x lebar x 3

print("\nContoh 2 baris x 3 kolom pertama (R, G, B):")
print(array_foto[0:2, 0:3])


# ==========================================
# 9. BUKTI: UBAH ANGKA, GAMBAR IKUT BERUBAH
# ==========================================

print("\n=== BUKTI UBAH ANGKA ===")

os.makedirs("hasil", exist_ok=True)

# Potongan 200 x 200 pixel dari tengah foto
tengah_x = lebar // 2
tengah_y = tinggi // 2

potongan = array_foto[
    max(tengah_y - 100, 0):tengah_y + 100,
    max(tengah_x - 100, 0):tengah_x + 100
].copy()

nama = os.path.splitext(os.path.basename(NAMA_FILE))[0]
file_asli = f"hasil/{nama}_potongan_asli.png"
file_ubah = f"hasil/{nama}_potongan_tanpa_hijau.png"

# Simpan potongan asli
Image.fromarray(potongan).save(file_asli)

# Ubah angkanya: hapus channel hijau (G = 0)
potongan[:, :, 1] = 0
Image.fromarray(potongan).save(file_ubah)

print("Potongan asli disimpan        :", file_asli)
print("Channel hijau diubah jadi 0   :", file_ubah)
print("Kesimpulan: angka diubah -> tampilan gambar ikut berubah")