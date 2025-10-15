import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from login_screen import LoginScreen
from menu import MenuWindow


class App(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B de Bet")

        # Tela de login
        self.tela_login = LoginScreen()
        self.addWidget(self.tela_login)

        # Conecta sinal de sucesso
        self.tela_login.login_sucesso.connect(self.abrir_menu)

        self.show()

    def abrir_menu(self, token):
        """Troca para a tela principal"""
        self.menu = MenuWindow(token)
        self.addWidget(self.menu)
        self.setCurrentWidget(self.menu)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = App()
    sys.exit(app.exec())
