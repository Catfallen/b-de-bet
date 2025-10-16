import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from qr_code import QrCodeWindow  # tela que mostra o QR

class DepositoWindow(QWidget):
    def __init__(self, token=""):
        super().__init__()
        self.token = token
        self.setWindowTitle("Depósito - B de Bet")
        self.setFixedSize(300, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.valor_input = QLineEdit()
        self.valor_input.setPlaceholderText("Valor (ex: 1.03)")
        layout.addWidget(self.valor_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Descrição")
        layout.addWidget(self.desc_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Seu email")
        layout.addWidget(self.email_input)

        btn_pagar = QPushButton("Gerar QR Code")
        btn_pagar.clicked.connect(self.pagar)
        layout.addWidget(btn_pagar)

        self.setLayout(layout)

    def pagar(self):
        valor = self.valor_input.text().strip()
        desc = self.desc_input.text().strip()
        email = self.email_input.text().strip()

        if not valor or not desc or not email:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        try:
            url = "http://localhost:3000/payments/pagar"
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "transaction_amount": float(valor),
                "description": desc,
            "payer_email": email
            }

            r = requests.post(url, json=payload, headers=headers)
            if r.status_code in (200, 201):
                dados = r.json()
                #print(dados)

            # Pegar qr_code_base64 e qr_code
                transaction = dados.get("transaction") or dados.get("sucess") or dados

                qr_payload = transaction.get('payload', {}) \
                .get('point_of_interaction', {}) \
                .get('transaction_data', {}) \
                .get('qr_code_base64')

            # fallback para QR em texto
                qr_text = transaction.get('payload', {}) \
                .get('point_of_interaction', {}) \
                .get('transaction_data', {}) \
                .get('qr_code')

                # Código alternativo, caso queira também o QR em texto
                #qr_text = transaction.get('point_of_interaction', {}).get('transaction_data', {}).get('qr_code',{})    
                print(f"""
                      ======================================================
                      qr_payload
                      {qr_payload}
                      ========================================================================================================================================================
                      qr_text
                      {qr_text}
                      ===========
                      """)
            # Abrir janela QR Code
                self.qr_window = QrCodeWindow(qr_text, qr_payload,valor,email)
                self.qr_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Erro", f"Falha no pagamento: {r.text}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao processar pagamento:\n{e}")
