import sqlite3

class DatabaseManager:
    def __init__(self, db_name="perpustakaan.db"):
        self.db_name = db_name
        self.conn = None
        self.connect()

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row 

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def init_db(self):
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
            cursor.execute("ALTER TABLE buku ADD COLUMN lokasi_rak TEXT")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass 
        self.conn.commit()

    def add_book(self, judul, penulis, kategori, lokasi_rak):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO buku (judul, penulis, kategori, status, lokasi_rak)
            VALUES (?, ?, ?, 'Tersedia', ?)
        ''', (judul, penulis, kategori, lokasi_rak))
        self.conn.commit()

    def get_books(self, keyword="", status_filter="Semua"):
        cursor = self.conn.cursor()
        query = "SELECT * FROM buku WHERE 1=1"
        params = []

        if keyword:
            if keyword.isdigit(): 
                query += " AND id = ?"
                params.append(int(keyword))
            else:
               
                query += " AND (LOWER(judul) LIKE ? OR LOWER(penulis) LIKE ? OR LOWER(lokasi_rak) LIKE ?)"
                params.append(f"%{keyword}%")
                params.append(f"%{keyword}%")
                params.append(f"%{keyword}%")
        
        if status_filter != "Semua":
        
            query += " AND status = ?"
            params.append(status_filter)

        cursor.execute(query, tuple(params))
        return cursor.fetchall()
        
    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM buku")
        return cursor.fetchall()

    def update_book(self, id_buku, judul, penulis, kategori, lokasi_rak):
        
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE buku SET judul=?, penulis=?, kategori=?, lokasi_rak=? WHERE id=?
        ''', (judul, penulis, kategori, lokasi_rak, id_buku))
        self.conn.commit()

    def delete_book(self, id_buku):
        
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM buku WHERE id=?", (id_buku,))
        self.conn.commit()

    def update_book_status(self, id_buku, new_status, tgl_pinjam=None, tgl_kembali=None):
        cursor = self.conn.cursor()
        if new_status == "Dipinjam":
            cursor.execute('''
                UPDATE buku SET status=?, tanggal_pinjam=?, tanggal_kembali=? WHERE id=?
            ''', (new_status, tgl_pinjam, tgl_kembali, id_buku))
        else: 
            cursor.execute('''
                UPDATE buku SET status=?, tanggal_pinjam=NULL, tanggal_kembali=NULL WHERE id=?
            ''', (new_status, id_buku))
        self.conn.commit()