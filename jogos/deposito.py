import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal
import utils  # ✅ importa o arquivo com o TOKEN global
from qrcode_tela import QrCodeWindow  # certifique-se de importar a classe

class DepositoWindow(QWidget):
    abrir_qrcode = pyqtSignal(dict, dict)  # sinal para abrir a tela do QR Code

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Depósito")
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        self.label_valor = QLabel("Valor do depósito:")
        self.input_valor = QLineEdit()
        self.input_valor.setPlaceholderText("Ex: 10.00")

        self.label_email = QLabel("E-mail do pagador:")
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Ex: teste@gmail.com")

        self.btn_depositar = QPushButton("Gerar QR Code")
        self.btn_depositar.clicked.connect(self.realizar_deposito)

        layout.addWidget(self.label_valor)
        layout.addWidget(self.input_valor)
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.btn_depositar)

        self.setLayout(layout)

    def realizar_deposito(self):
        valor = self.input_valor.text().strip()
        email = self.input_email.text().strip()

        if not valor or not email:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        if not utils.TOKEN:
            QMessageBox.critical(self, "Erro", "Token de autenticação não encontrado. Faça login novamente.")
            return

        try:
            data = {
                "transaction_amount": float(valor),
                "description": "Depósito no B de Bet",
                "payer_email": email
            }

            headers = {
                "Authorization": f"Bearer {utils.TOKEN}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                "http://localhost:3000/payments/pagar",
                json=data,
                headers=headers
            )

            if response.status_code in (200, 201):
                try:
                    dados = response.json()
                    print("dados:", dados)

                    # Aqui abrimos a janela diretamente, sem usar sinal
                    self.qr_window = QrCodeWindow(dados, data)
                    self.qr_window.show()

                except ValueError:
                    QMessageBox.warning(self, "Erro", "Resposta inválida do servidor.")
            else:
                try:
                    err = response.json().get("error", response.text)
                except ValueError:
                    err = response.text
                QMessageBox.warning(self, "Erro", f"Falha ao processar pagamento ({response.status_code})\n{err}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {str(e)}")
