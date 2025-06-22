from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from main_window_app import Perpustakaan
from Database_manager import DatabaseManager


class LoginDialog(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("ui/login.ui", self)
        self.setWindowTitle("Login Sistem Perpustakaan")

        self.login_gambar.setPixmap(QPixmap("gambar/icon_judul.png").scaled(100, 100))
        self.correct_username = "dewiagustina"
        self.correct_password = "dewi123"

        self.error_label.hide()
        self.btn_login.clicked.connect(self.check_login)

        self.username_input.setPlaceholderText("Masukkan username")
        self.password_input.setPlaceholderText("Masukkan password")
        self.password_input.setEchoMode(self.password_input.Password)

    def check_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.error_label.setText("Username dan Password harus diisi.")
            self.error_label.show()
            return

        if username == self.correct_username and password == self.correct_password:

            db_manager = DatabaseManager("perpustakaan.db")
            db_manager.init_db()
            
            self.main_window = Perpustakaan(db_manager)
            self.main_window.show()
            self.close()  
            
        else:
            self.error_label.setText("Username atau Password salah.")
            self.error_label.show()
            self.password_input.clear()
            self.username_input.setFocus()
