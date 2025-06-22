from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/menu_about.ui",self)
        self.setWindowTitle("Tentang Aplikasi")
        self.setStyleSheet("""
                           #buttonBox QPushButton {
                                background-color: #1167b1;
                                color: white;
                                padding: 6px 12px;
                                border-radius: 4px;
                            }

                            #buttonBox QPushButton:hover {
                                background-color: #0e5492;
                            }
        """)