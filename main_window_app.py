import sqlite3
import csv
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox,
    QFileDialog, QHeaderView, QDateEdit, QMenuBar, QAction, QDialog, QDialogButtonBox # QDialog dan QDialogButtonBox diimpor juga tapi tidak digunakan langsung di sini
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from Tambah_Buku import BookFormDialog
from Database_manager import DatabaseManager

class Perpustakaan(QMainWindow):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        loadUi("ui/main_window.ui", self) 
        self.setWindowTitle("Sistem Manajemen Perpustakaan")
        self.db_manager=db_manager
        self.db=self.db_manager.conn
        
        self.gambar_judul.setPixmap(QPixmap("gambar/icon_judul.png").scaled(60,60))
    
        self.export_action.triggered.connect(self.export_csv)
        self.exit_action.triggered.connect(self.close)
        self.add_action.triggered.connect(self.tambah_buku)
        self.edit_action.triggered.connect(self.edit_buku_dialog)
        self.delete_action.triggered.connect(self.hapus_buku)
        self.change_status_action.triggered.connect(self.ubah_status_buku_via_menu)
        
        self.btn_tambah.clicked.connect(self.tambah_buku)
        self.btn_tambah.setCursor(Qt.PointingHandCursor) 
        
        self.title_label.setAlignment(Qt.AlignCenter)
        stats_cards_layout = QHBoxLayout(self.card_container)
        stats_cards_layout.setSpacing(20) 
        stats_cards_layout.setContentsMargins(0, 10, 0, 20) 
        self.card_total_buku = self.stat_card("Total Buku", "0", "#03254c", "#ffffff", "total_buku_val")
        stats_cards_layout.addWidget(self.card_total_buku)

        self.card_dipinjam = self.stat_card("Dipinjam", "0", "#03254c", "#ffffff", "dipinjam_val")
        stats_cards_layout.addWidget(self.card_dipinjam)

        self.card_tersedia = self.stat_card("Tersedia", "0", "#03254c", "#ffffff", "tersedia_val")
        stats_cards_layout.addWidget(self.card_tersedia)

        self.search_input.textChanged.connect(self.load_data)
        self.filter_status.currentIndexChanged.connect(self.load_data)
        self.filter_status.setToolTip("Filter bedasarkan status Buku")
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive) # ID
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive) # Judul
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive) # Penulis
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive) # Kategori
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Interactive) # Status
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Interactive) # Tgl Pinjam
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Interactive) # Tgl Kembali
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Interactive) # Denda
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.Interactive) # Lokasi Rak
        self.table.horizontalHeader().setSectionResizeMode(9, QHeaderView.Stretch) # Kolom Aksi akan meregang
        
        self.table.setSelectionBehavior(QTableWidget.SelectRows) 
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.table.horizontalHeader().setSectionsMovable(False) 

        label_nama= QLabel("Dewi Agustin Asri | F1D022039")
        label_nama.setStyleSheet("color: #000000;font-size:10pt;padding:5px;font-weight:bold")
        label_nama.setAlignment(Qt.AlignCenter) 
        self.statusbar = self.statusBar()
        self.statusbar.setFixedHeight(50)
        self.statusbar.setFixedWidth(900)
        self.statusbar.addPermanentWidget(label_nama) 
        
        self.load_data()
    def stat_card(self, title, value, bg_color, text_color, value_object_name):
        card_widget = QWidget()
        card_layout = QVBoxLayout(card_widget)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {text_color}; border: none;") 
        card_layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setObjectName(value_object_name) 
        value_label.setStyleSheet(f"font-size: 38px; font-weight: bold; color: {text_color}; margin-top: 5px; border: none;") 
        card_layout.addWidget(value_label)

        card_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 15px;
                border: 1px solid #ced4da; 
            }}
        """)
        return card_widget

    def ubah_status_db(self, id_buku, new_status, tgl_pinjam=None, tgl_kembali=None):
        try:
            self.db_manager.update_book_status(id_buku, new_status, tgl_pinjam, tgl_kembali)
            QMessageBox.information(self, "Berhasil", f"Status buku berhasil diperbarui menjadi '{new_status}'.", QMessageBox.Ok)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat memperbarui status buku: {e}", QMessageBox.Ok)

    def ubah_status_dropdown(self, book_id, judul_buku, old_status, new_status_text, combo_box):
        if new_status_text == old_status:
            return
        combo_box.blockSignals(True)

        if new_status_text == "Dipinjam":
            date_edit = QDateEdit(QDate.currentDate().addDays(7)) 
            date_edit.setCalendarPopup(True)
            date_edit.setDisplayFormat("yyyy-MM-dd")
            
            msg_box_layout = QVBoxLayout()
            msg_box_layout.addWidget(QLabel("Tanggal Kembali (YYYY-MM-DD):"))
            msg_box_layout.addWidget(date_edit)
            
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setWindowTitle("Konfirmasi Tanggal Kembali")
            msg_box.setText(f"Pilih tanggal pengembalian untuk '{judul_buku}':")
            msg_box_widget = QWidget()
            msg_box_widget.setLayout(msg_box_layout)
            msg_box.layout().addWidget(msg_box_widget) 
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
            ret = msg_box.exec_() 

            if ret == QMessageBox.Ok:
                tgl_pinjam = datetime.now().strftime("%Y-%m-%d")
                tgl_kembali = date_edit.date().toString("yyyy-MM-dd")
                self.ubah_status_db(book_id, new_status_text, tgl_pinjam, tgl_kembali)
            else:
                combo_box.setCurrentText(old_status)
        else: 
            self.ubah_status_db(book_id, new_status_text)
        
        combo_box.blockSignals(False) 

    def load_data(self):
        keyword = self.search_input.text().lower().strip()
        status_filter = self.filter_status.currentText()
        buku_list = self.db_manager.get_books(keyword, status_filter)

        self.table.setRowCount(0)
        total_buku = 0
        total_dipinjam = 0
        total_tersedia = 0 

        for row_data in buku_list:
            total_buku += 1
            if row_data[4] == "Dipinjam":
                total_dipinjam += 1
            else:
                total_tersedia += 1 

            row = self.table.rowCount()
            self.table.insertRow(row)
            for col_idx in [0, 1, 2, 3, 5, 6]:
                item_text = str(row_data[col_idx]) if row_data[col_idx] is not None else "-"
                item = QTableWidgetItem(item_text)
                item.setFlags(item.flags() | Qt.TextWordWrap) 
                self.table.setItem(row, col_idx, item)
  
            status_combo_box = QComboBox()
            status_combo_box.addItems(["Tersedia", "Dipinjam"])
            current_status = str(row_data[4]) if row_data[4] is not None else "Tersedia"
            status_combo_box.setCurrentText(current_status)
  
            try:
                status_combo_box.currentIndexChanged.disconnect()
            except TypeError:
                pass 
 
            book_id = row_data[0]
            judul_buku = row_data[1]
            status_combo_box.currentIndexChanged.connect(
     
                lambda index, b_id=book_id, j_buku=judul_buku, old_stat=current_status, cb=status_combo_box: 
                self.ubah_status_dropdown(b_id, j_buku, old_stat, cb.currentText(), cb)
            )
            self.table.setCellWidget(row, 4, status_combo_box) 
            denda = "-"
            if row_data[4] == "Dipinjam" and row_data[6]: 
                try:
                    tgl_kembali_str = row_data[6]
                    if tgl_kembali_str: 
                        tgl_kembali = datetime.strptime(tgl_kembali_str, "%Y-%m-%d")
                        selisih = (datetime.now() - tgl_kembali).days
                        if selisih > 0: 
                            denda = f"Rp {selisih * 1000}" 
                except ValueError:
                    denda = "Tanggal invalid" 
            item_denda = QTableWidgetItem(denda)
            item_denda.setFlags(item_denda.flags() | Qt.TextWordWrap)
            self.table.setItem(row, 7, item_denda)
            item_lokasi_rak = QTableWidgetItem(str(row_data[7]) if row_data[7] is not None else "-")
            item_lokasi_rak.setFlags(item_lokasi_rak.flags() | Qt.TextWordWrap)
            self.table.setItem(row, 8, item_lokasi_rak) 
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0) 
            action_layout.setSpacing(5) 

            btn_edit_row = QPushButton("Edit")
            btn_edit_row.setStyleSheet("""
                QPushButton { background-color: #1167b1; color: white; border-radius: 5px; padding: 5px 8px; font-size: 18px; border: none; }
                QPushButton:hover { background-color: #2a9df4; }
            """)
            btn_edit_row.setCursor(Qt.PointingHandCursor)
            btn_edit_row.clicked.connect(lambda _, r=row: self.edit_buku_dialog_from_row(r))
            action_layout.addWidget(btn_edit_row)

            btn_delete_row = QPushButton("Hapus")
            btn_delete_row.setStyleSheet("""
                QPushButton { background-color: #E74C3C; color: white; border-radius: 5px; padding: 5px 8px; font-size: 18px; border: none; }
                QPushButton:hover { background-color: #C0392B; }
                QPushButton:pressed { background-color: #A93226; }
            """)
            btn_delete_row.setCursor(Qt.PointingHandCursor)
            btn_delete_row.clicked.connect(lambda _, r=row: self.hapus_buku_from_row(r))
            action_layout.addWidget(btn_delete_row)

            self.table.setCellWidget(row, 9, action_widget) 

        self.card_total_buku.findChild(QLabel, "total_buku_val").setText(str(total_buku))
        self.card_dipinjam.findChild(QLabel, "dipinjam_val").setText(str(total_dipinjam))
        self.card_tersedia.findChild(QLabel, "tersedia_val").setText(str(total_tersedia))

        self.table.resizeColumnsToContents() 
        self.table.resizeRowsToContents() 
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(self.table.columnCount() - 1, QHeaderView.Stretch)

    def ubah_status_buku_via_menu(self):
        """Memicu perubahan status buku dari menu bar (dengan memilih baris)."""
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Peringatan", "Pilih buku yang ingin diubah statusnya dari tabel.", QMessageBox.Ok)
            return
        row = selected_rows[0].row()
        self.ubah_status_buku(row) 

    def ubah_status_buku(self, row):
        combo_box = self.table.cellWidget(row, 4) 
        if isinstance(combo_box, QComboBox):
            combo_box.showPopup() 
        else:
            QMessageBox.warning(self, "Error", "Status kolom bukan dropdown.", QMessageBox.Ok)

    def edit_buku_dialog_from_row(self, row):
        """Membuka dialog edit buku dengan data dari baris tabel tertentu."""
        id_buku = self.table.item(row, 0).text()
        judul_lama = self.table.item(row, 1).text()
        penulis_lama = self.table.item(row, 2).text()
        kategori_lama = self.table.item(row, 3).text()
        lokasi_rak_lama = self.table.item(row, 8).text() 
        dialog = BookFormDialog(judul_lama, penulis_lama, kategori_lama, lokasi_rak_lama, self)
        
        if dialog.exec_() == QDialog.Accepted:
            new_data = dialog.get_data()
            ok_judul = new_data["judul"]
            ok_penulis = new_data["penulis"]
            ok_kategori = new_data["kategori"]
            ok_lokasi_rak = new_data["lokasi_rak"]
            if not ok_judul or not ok_penulis:
                QMessageBox.warning(self, "Input Error", "Judul dan Penulis harus diisi.", QMessageBox.Ok)
                return

            try:
                self.db_manager.update_book(id_buku, ok_judul, ok_penulis, ok_kategori, ok_lokasi_rak)
                QMessageBox.information(self, "Berhasil", "Detail buku berhasil diperbarui.", QMessageBox.Ok)
                self.load_data() 
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat memperbarui buku: {e}", QMessageBox.Ok)

    def edit_buku_dialog(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Peringatan", "Pilih buku yang ingin diedit dari tabel.", QMessageBox.Ok)
            return
        
        self.edit_buku_dialog_from_row(selected_rows[0].row())

    def hapus_buku_from_row(self, row):

        id_buku = self.table.item(row, 0).text()
        judul_buku = self.table.item(row, 1).text()
        reply = QMessageBox.question(self, "Konfirmasi Hapus", 
                                     f"Anda yakin ingin menghapus buku '{judul_buku}'?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.db_manager.delete_book(id_buku)
                QMessageBox.information(self, "Berhasil", "Buku berhasil dihapus!", QMessageBox.Ok)
                self.load_data() # Muat ulang data
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat menghapus buku: {e}", QMessageBox.Ok)

    def hapus_buku(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Peringatan", "Pilih buku yang ingin dihapus dari tabel.", QMessageBox.Ok)
            return
        self.hapus_buku_from_row(selected_rows[0].row())
        
    def tambah_buku(self):
        dialog = BookFormDialog(parent=self) 
        if dialog.exec_() == QDialog.Accepted: # Jika dialog diterima
            new_data = dialog.get_data()
            judul = new_data["judul"]
            penulis = new_data["penulis"]
            kategori = new_data["kategori"]
            lokasi_rak = new_data["lokasi_rak"]
            if not judul or not penulis:
                QMessageBox.warning(self, "Input Error", "Judul dan Penulis harus diisi.", QMessageBox.Ok)
                return

            try:
                self.db_manager.add_book(judul, penulis, kategori, lokasi_rak)
                QMessageBox.information(self, "Berhasil", "Buku berhasil ditambahkan!", QMessageBox.Ok)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat menambahkan buku: {e}", QMessageBox.Ok)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan CSV", "data_buku.csv", "CSV Files (*.csv)")
        if path:
            try:
                data = self.db_manager.get_all_books() 
                with open(path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Judul", "Penulis", "Kategori", "Status", "Tgl Pinjam", "Tgl Kembali", "Denda (Saat Export)", "Lokasi Rak"])
                    
                    for row_data in data:
                        denda = "-"
                        if row_data[4] == "Dipinjam" and row_data[6]:
                            try:
                                tgl_kembali_str = row_data[6]
                                if tgl_kembali_str:
                                    tgl_kembali = datetime.strptime(tgl_kembali_str, "%Y-%m-%d")
                                    selisih = (datetime.now() - tgl_kembali).days
                                    if selisih > 0:
                                        denda = f"Rp {selisih * 1000}"
                            except ValueError:
                                denda = "Tanggal invalid"
                    
                        row_to_write = list(row_data[:7]) + [denda, row_data[7]]
                        writer.writerow(row_to_write)

                QMessageBox.information(self, "Export Berhasil", "Data berhasil diexport ke CSV!", QMessageBox.Ok)
            except IOError as e:
                QMessageBox.critical(self, "Error", f"Tidak dapat menulis file: {e}", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Terjadi kesalahan tidak terduga saat export: {e}", QMessageBox.Ok)