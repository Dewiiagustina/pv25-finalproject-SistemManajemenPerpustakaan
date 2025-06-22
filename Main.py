import sys
from PyQt5.QtWidgets import QApplication
from Login import LoginDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginDialog()
    login_window.show()  
    sys.exit(app.exec_())
