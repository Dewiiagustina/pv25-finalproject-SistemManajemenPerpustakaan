# Sistem Manajemen Perpustakaan

Aplikasi desktop berbasis **PyQt5** dan **SQLite** untuk mengelola data buku dalam sebuah perpustakaan. Aplikasi ini dirancang untuk mempermudah proses pendataan buku, pencatatan peminjaman dan pengembalian, serta menampilkan statistik koleksi buku dengan antarmuka yang interaktif dan mudah digunakan.

---

##  Fitur Utama

- ** Login Otentikasi**  
  Form login untuk membatasi akses pengguna ke sistem.

- ** Dashboard Interaktif**  
  Menampilkan statistik jumlah buku total, buku dipinjam, dan buku tersedia dalam bentuk kartu info.

- ** Manajemen Buku (CRUD)**  
  - Tambah data buku baru  
  - Edit data buku yang sudah ada  
  - Hapus data buku dengan konfirmasi  
  - Informasi mencakup judul, penulis, kategori, status, dan lokasi rak.

- ** Peminjaman dan Pengembalian Buku**  
  - Ubah status buku menjadi *Dipinjam* atau *Tersedia*  
  - Tanggal kembali dipilih otomatis melalui kalender  
  - Data peminjaman disimpan ke database.

- ** Perhitungan Denda Otomatis**  
  - Denda dihitung otomatis berdasarkan selisih hari dari tanggal kembali  
  - Tarif denda: **Rp 1.000/hari keterlambatan**  
  - Denda ditampilkan di tabel dan saat ekspor.

- ** Ekspor Data ke CSV**  
  - Seluruh data buku dapat diekspor ke file `.csv`  
  - Termasuk informasi denda dan lokasi rak.

- ** Tentang Aplikasi (About)**  
  - Dialog informasi pengembang dan detail proyek.

---

## 🛠️ Teknologi yang Digunakan

- Python 3.x
- PyQt5
- SQLite3
- Qt Designer (.ui files)

---

## 🖥️ Tampilan Antarmuka

> Beberapa tampilan aplikasi:
- Form Login
  ![login](https://github.com/user-attachments/assets/720c33cc-9bc7-4bcc-ab66-4d03caaa5f62)
- Dashboard
  ![dashboard](https://github.com/user-attachments/assets/7c2542ba-3be9-4af1-9d00-33697d27d400)
- Dialog Tambah/Edit Buku
  ![tambah buku](https://github.com/user-attachments/assets/a2b4e503-a614-4c72-89dd-227f1153949c)

- Dialog Tentang Aplikasi
![about](https://github.com/user-attachments/assets/c184de09-a157-401d-b2a8-e106ab2a2920)
