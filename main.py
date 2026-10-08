from PIL import Image
from PIL.ExifTags import TAGS
from pillow_heif import register_heif_opener
import numpy as np

register_heif_opener()

# ==========================================
# 1. MEMBUKA FOTO
# ==========================================

foto = Image.open("cam.jpeg")


# ==========================================
# 2. INFORMASI DASAR FOTO
# ==========================================

print("=== INFORMASI FOTO ===")

print("Nama file      :", foto.filename)
print("Format         :", foto.format)
print("Ukuran         :", foto.size)
print("Mode warna     :", foto.mode)

# Mengambil lebar dan tinggi gambar
lebar, tinggi = foto.size

# Menghitung jumlah pixel
jumlah_pixel = lebar * tinggi

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

for nama_tag in tag_pilihan:
    if nama_tag in semua_exif:
        print(nama_tag, ":", semua_exif[nama_tag])


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

if foto.mode == "RGB":

    r, g, b = pixel

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
array_foto = np.array(foto)

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

# Ambil potongan 200 x 200 pixel dari pojok kiri atas
potongan = array_foto[0:200, 0:200].copy()

# Simpan potongan asli
Image.fromarray(potongan).save("potongan_asli.png")

# Ubah angkanya: hapus channel hijau (G = 0)
potongan[:, :, 1] = 0
Image.fromarray(potongan).save("potongan_tanpa_hijau.png")

print("Potongan asli disimpan        : potongan_asli.png")
print("Channel hijau diubah jadi 0   : potongan_tanpa_hijau.png")
print("Kesimpulan: angka diubah -> tampilan gambar ikut berubah")