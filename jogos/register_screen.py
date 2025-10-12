# register_screen.py
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils import API_URL, TOKEN

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
            try:
                res_json = response.json()
            except ValueError:
                QMessageBox.critical(self, "Erro", f"Resposta inválida da API: {response.text}")
                return

            if response.status_code == 201:
                TOKEN = res_json.get("token")
                QMessageBox.information(self, "Sucesso", "Registro realizado com sucesso!")
                self.stack.setCurrentIndex(2)
            else:
                QMessageBox.warning(self, "Erro", res_json.get("error", "Falha no registro"))

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar à API.")
