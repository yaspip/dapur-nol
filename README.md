# Dapur Nol

Panduan mengenal makanan dari nol: bahan dan bumbu, rasa, Kitchen Gems, resep pemula dengan mode masak, isi dapur, dan daftar belanja. Dibuat sebagai PWA, jadi bisa dipasang di HP dan dibuka offline.

## Struktur

| Path | Isi |
| --- | --- |
| `index.html` | Aplikasi (hasil build, jangan diedit langsung) |
| `manifest.webmanifest` | Nama, warna, ikon saat dipasang |
| `sw.js` | Service worker: offline + ambil versi terbaru saat online |
| `icons/` | Ikon aplikasi |
| `src/dapur-nol.html` | Sumber aplikasi (edit di sini) |
| `tools/build_pwa.py` | Membangun `index.html`, `manifest.webmanifest`, `sw.js` dari sumber |

## Memperbarui

1. Edit `src/dapur-nol.html`.
2. Jalankan `python3 tools/build_pwa.py`.
3. Commit dan push ke `main`. GitHub Pages menayangkan versi baru dalam ±1 menit, dan app di HP mengambilnya saat dibuka berikutnya.

## Data pengguna

Isi dapur, belanja, simpanan, dan progres tersimpan di browser HP masing-masing (localStorage), tidak di repository ini. Gunakan Dapurku → Pengaturan → Salin cadangan untuk memindahkannya.

## Konten

Resep ditulis ulang dari pengetahuan masak umum. Kitchen Gems menautkan sumber publik (USDA, FDA, WHO, Kemenkes, dan lainnya) di halaman masing-masing. Harga adalah contoh kisaran, bukan harga resmi.
