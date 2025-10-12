import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import pyqtSignal


class DepositoWindow(QWidget):
    abrir_qrcode = pyqtSignal(dict,dict)  # sinal para abrir a tela do QR Code

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

        try:
            data = {
                "transaction_amount": float(valor),
                "description": "Depósito no B de Bet",
                "payer_email": email
            }

            response = requests.post("http://localhost:3000/pagar", json=data)

            if response.status_code in (200,201):
                try:
                    dados = response.json()
                    print('dados')
                    self.abrir_qrcode.emit(dados,data)  # envia dados para a tela de QR
                except ValueError:
                    QMessageBox.warning(self, "Erro", "Resposta inválida do servidor.")
            else:
                QMessageBox.warning(self, "Erro", f"Falha ao processar pagamento ({response.status_code})")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {str(e)}")