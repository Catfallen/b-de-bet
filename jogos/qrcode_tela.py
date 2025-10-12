import base64
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray, Qt


class QrCodeWindow(QWidget):
    def __init__(self, dados,data):
        super().__init__()
        self.setWindowTitle("Leitura do QR Code")
        self.setGeometry(100, 100, 350, 400)

        layout = QVBoxLayout()
        print(data)
        valor = data.get("transaction_amount", 0)
        email = data.get("payer_email", "")
        qr_code_base64 = dados.get("qr_code_base64")
        qr_text = dados.get("qr_code")

        # Exibe informações básicas
        info_label = QLabel(f"<b>Depósito:</b> R${valor:.2f}<br><b>Email:</b> {email}")
        info_label.setStyleSheet("font-size: 14px; text-align: center;")
        layout.addWidget(info_label)

        # Exibir QR Code
        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if qr_code_base64:
            try:
                # Decodifica o Base64 e carrega no QPixmap
                qr_bytes = base64.b64decode(qr_code_base64)
                #print(qr_bytes)
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(qr_bytes))
                qr_label.setPixmap(pixmap.scaled(250, 250))
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Falha ao carregar QR Code: {str(e)}")
        else:
            qr_label.setText("⚠️ QR Code não encontrado na resposta da API.")

        layout.addWidget(qr_label)

        # Exibir código PIX em texto (caso o usuário queira copiar manualmente)
        pix_label = QLabel(f"<b>Código PIX:</b><br>{qr_text}")
        pix_label.setStyleSheet("font-size: 12px; text-align: center;")
        layout.addWidget(pix_label)

        # Botão para voltar
        self.btn_voltar = QPushButton("Voltar ao menu")
        layout.addWidget(self.btn_voltar)

        self.setLayout(layout)
