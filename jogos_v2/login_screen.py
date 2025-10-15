import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal


class LoginScreen(QWidget):
    # Sinal para abrir a próxima tela (envia o token opcionalmente)
    login_sucesso = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login / Registro - B de Bet")
        self.setFixedSize(320, 300)

        self.mode = "login"  # alterna entre login e registro
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title = QLabel("Login")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title)

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome (somente para registro)")
        self.nome_input.hide()
        layout.addWidget(self.nome_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.senha_input)

        self.btn_acao = QPushButton("Entrar")
        self.btn_acao.clicked.connect(self.enviar_requisicao)
        layout.addWidget(self.btn_acao)

        self.btn_alternar = QPushButton("Criar conta")
        self.btn_alternar.clicked.connect(self.alternar_modo)
        layout.addWidget(self.btn_alternar)

        self.setLayout(layout)

    def alternar_modo(self):
        """Alterna entre Login e Registro"""
        if self.mode == "login":
            self.mode = "register"
            self.title.setText("Registro")
            self.btn_acao.setText("Registrar")
            self.btn_alternar.setText("Já tenho conta")
            self.nome_input.show()
        else:
            self.mode = "login"
            self.title.setText("Login")
            self.btn_acao.setText("Entrar")
            self.btn_alternar.setText("Criar conta")
            self.nome_input.hide()

    def enviar_requisicao(self):
        """Envia POST para a API e abre o menu se sucesso"""
        email = self.email_input.text().strip()
        senha = self.senha_input.text().strip()
        nome = self.nome_input.text().strip()

        if not email or not senha or (self.mode == "register" and not nome):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos necessários.")
            return

        url = f"http://localhost:3000/auth/{self.mode}"
        dados = {"email": email, "senha": senha}
        if self.mode == "register":
            dados["nome"] = nome

        try:
            r = requests.post(url, json=dados)

            if r.status_code == 200:
                data = r.json()
                token = data.get("token", "")
                QMessageBox.information(self, "Sucesso", f"{self.mode.title()} realizado com sucesso!")
                self.login_sucesso.emit(token)
            else:
                QMessageBox.warning(self, "Erro", f"Falha no {self.mode}: {r.text}")

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar à API em localhost:3000.")
