import sqlite3

class DatabaseManager:
    def __init__(self, db_name="perpustakaan.db"):
        self.db_name = db_name
        self.conn = None
        self.connect()

    def connect(self):
        """Membangun koneksi ke database SQLite."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row # Memungkinkan akses kolom berdasarkan nama

    def close(self):
        """Menutup koneksi database."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def init_db(self):
        """Menginisialisasi skema database (membuat tabel jika belum ada)."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buku(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judul TEXT,
                penulis TEXT,
                kategori TEXT,
                status TEXT,
                tanggal_pinjam TEXT,
                tanggal_kembali TEXT,
                lokasi_rak TEXT
            )
        ''')
        try:
            # Mencoba menambahkan kolom lokasi_rak jika belum ada
            cursor.execute("ALTER TABLE buku ADD COLUMN lokasi_rak TEXT")
            self.conn.commit()
        except sqlite3.OperationalError:
            # Jika kolom sudah ada, akan ada OperationalError, abaikan
            pass 
        self.conn.commit()

    def add_book(self, judul, penulis, kategori, lokasi_rak):
        """Menambahkan buku baru ke database."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO buku (judul, penulis, kategori, status, lokasi_rak)
            VALUES (?, ?, ?, 'Tersedia', ?)
        ''', (judul, penulis, kategori, lokasi_rak))
        self.conn.commit()

    def get_books(self, keyword="", status_filter="Semua"):
        """Mengambil daftar buku dari database berdasarkan keyword dan filter status."""
        cursor = self.conn.cursor()
        query = "SELECT * FROM buku WHERE 1=1"
        params = []

        if keyword:
            if keyword.isdigit(): 
                # Jika keyword adalah angka, cari berdasarkan ID
                query += " AND id = ?"
                params.append(int(keyword))
            else:
                # Jika keyword bukan angka, cari di judul, penulis, atau lokasi rak (case-insensitive)
                query += " AND (LOWER(judul) LIKE ? OR LOWER(penulis) LIKE ? OR LOWER(lokasi_rak) LIKE ?)"
                params.append(f"%{keyword}%")
                params.append(f"%{keyword}%")
                params.append(f"%{keyword}%")
        
        if status_filter != "Semua":
            # Filter berdasarkan status jika tidak 'Semua'
            query += " AND status = ?"
            params.append(status_filter)

        cursor.execute(query, tuple(params))
        return cursor.fetchall()
        
    def get_all_books(self):
        """Mengambil semua buku dari database (digunakan untuk ekspor CSV)."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM buku")
        return cursor.fetchall()

    def update_book(self, id_buku, judul, penulis, kategori, lokasi_rak):
        """Memperbarui detail buku yang sudah ada."""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE buku SET judul=?, penulis=?, kategori=?, lokasi_rak=? WHERE id=?
        ''', (judul, penulis, kategori, lokasi_rak, id_buku))
        self.conn.commit()

    def delete_book(self, id_buku):
        """Menghapus buku dari database."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM buku WHERE id=?", (id_buku,))
        self.conn.commit()

    def update_book_status(self, id_buku, new_status, tgl_pinjam=None, tgl_kembali=None):
        """Memperbarui status pinjam buku dan tanggal terkait."""
        cursor = self.conn.cursor()
        if new_status == "Dipinjam":
            cursor.execute('''
                UPDATE buku SET status=?, tanggal_pinjam=?, tanggal_kembali=? WHERE id=?
            ''', (new_status, tgl_pinjam, tgl_kembali, id_buku))
        else: # Jika status baru adalah "Tersedia"
            cursor.execute('''
                UPDATE buku SET status=?, tanggal_pinjam=NULL, tanggal_kembali=NULL WHERE id=?
            ''', (new_status, id_buku))
        self.conn.commit()