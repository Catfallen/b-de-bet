import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QStackedWidget, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from mines import MinesGame
# Variável global para armazenar o token JWT
TOKEN = None

API_URL = "http://localhost:3000/auth/"

# --------------------- Login ---------------------
class LoginScreen(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Login"))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        btn_login = QPushButton("Entrar")
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login)

        btn_register = QPushButton("Ir para Registro")
        btn_register.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def login(self):
        global TOKEN
        data = {
            "email": self.email_input.text(),
            "senha": self.password_input.text()
        }
        try:
            response = requests.post(API_URL + "login", json=data)
            if response.status_code == 200:
                TOKEN = response.json().get("token")
                QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
                self.stack.setCurrentIndex(2)  # Vai para o menu principal
            else:
                QMessageBox.warning(self, "Erro", response.json().get("error", "Falha no login"))
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar à API.")


# --------------------- Registro ---------------------
class RegisterScreen(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Registro"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome")
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        btn_register = QPushButton("Registrar")
        btn_register.clicked.connect(self.register)
        layout.addWidget(btn_register)

        btn_login = QPushButton("Ir para Login")
        btn_login.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def register(self):
        global TOKEN
        data = {
            "nome": self.name_input.text(),
            "email": self.email_input.text(),
            "senha": self.password_input.text()
        }
        try:
            response = requests.post(API_URL + "register", json=data)
            if response.status_code == 201:
                TOKEN = response.json().get("token")
                QMessageBox.information(self, "Sucesso", "Registro realizado com sucesso!")
                self.stack.setCurrentIndex(2)  # Vai para o menu principal
            else:
                QMessageBox.warning(self, "Erro", response.json().get("error", "Falha no registro"))
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar à API.")


# --------------------- Menu Principal ---------------------
class MenuScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Menu Principal - Selecione o Jogo"))

        self.games_list = QListWidget()
        self.games_list.addItems(["💣 Mines", "🚀 Crash", "🎰 Slot"])  # Pode adicionar mais
        layout.addWidget(self.games_list)

        btn_play = QPushButton("Jogar")
        btn_play.clicked.connect(self.play_game)
        layout.addWidget(btn_play)

        self.setLayout(layout)

    def play_game(self):
        game = self.games_list.currentItem()
        if game:
            QMessageBox.information(self, "Jogo selecionado", f"Você selecionou {game.text()}")
            # Aqui você pode abrir o widget correspondente ao jogo
            print("Mines" in str(game.text()))
            if "Mines" in str(game.text()):
                MinesGame()
            else:
                print(f"{game.text()} não é igual a {'Mines'}")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um jogo primeiro.")


# --------------------- App Principal ---------------------
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Casa de Apostas")
        self.setFixedSize(400, 400)

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


# --------------------- Inicialização ---------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
