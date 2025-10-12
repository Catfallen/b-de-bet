# main.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from login_screen import LoginScreen
from register_screen import RegisterScreen
from menu_screen import MenuScreen

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Casa de Apostas")
        self.setFixedSize(400, 500)

        self.stack = QStackedWidget()
        self.login_screen = LoginScreen(self.stack)
        self.register_screen = RegisterScreen(self.stack)
        self.menu_screen = MenuScreen()

        self.stack.addWidget(self.login_screen)    # index 0
        self.stack.addWidget(self.register_screen) # index 1
        self.stack.addWidget(self.menu_screen)     # index 2

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())