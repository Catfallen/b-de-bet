# login_screen.py
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils import API_URL, TOKEN

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
            try:
                res_json = response.json()
            except ValueError:
                QMessageBox.critical(self, "Erro", f"Resposta inválida da API: {response.text}")
                return

            if response.status_code == 200:
                TOKEN = res_json.get("token")
                QMessageBox.information(self, "Sucesso", "Login realizado com sucesso!")
                self.stack.setCurrentIndex(2)
            else:
                QMessageBox.warning(self, "Erro", res_json.get("error", "Falha no login"))

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar à API.")
