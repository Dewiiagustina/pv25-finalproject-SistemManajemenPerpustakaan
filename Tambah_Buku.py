from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt 

class BookFormDialog(QDialog):
    def __init__(self, judul="", penulis="", kategori="", lokasi_rak="", parent=None):
        super().__init__(parent)
        loadUi("ui/add_edit_buku.ui",self) 
        self.setWindowTitle("Tambah/Edit Buku")
        self.judul_label.setFixedWidth(80) 
        self.edit_judul.setPlaceholderText("Judul Buku")

        self.penulis_label.setFixedWidth(80)
        self.edit_penulis.setPlaceholderText("Penulis")
        
        self.kategori_label.setFixedWidth(80)
        self.edit_kategori.setCurrentText(kategori)
        self.edit_kategori.setToolTip("Pilih kategori buku")
        
        self.lokasi_rak_label.setFixedWidth(80)
        self.edit_lokasi_rak.setPlaceholderText("Lokasi Rak (e.g., A1, B2)")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
    
        self.edit_judul.setText(judul)
        self.edit_penulis.setText(penulis)
    
        self.edit_kategori.setCurrentText(kategori) 
        self.edit_lokasi_rak.setText(lokasi_rak)

    def get_data(self):
        return {
            "judul": self.edit_judul.text().strip(),        
            "penulis": self.edit_penulis.text().strip(),    
            "kategori": self.edit_kategori.currentText(),   
            "lokasi_rak": self.edit_lokasi_rak.text().strip() 
        }