import base64
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class QrCodeWindow(QWidget):
    def __init__(self, dados, data):
        super().__init__()
        self.setWindowTitle("Leitura do QR Code")
        self.setGeometry(100, 100, 350, 400)

        layout = QVBoxLayout()
        print("Dados recebidos:", dados)
        print("Data recebida:", data)

        valor = data.get("transaction_amount", 0)
        email = data.get("payer_email", "")
        qr_code_base64 = dados.get("payload", {}).get("qr_code_base64")
        qr_text = dados.get("qr_code") or dados.get("payload", {}).get("qr_code")

        # Exibe informações básicas
        info_label = QLabel(f"<b>Depósito:</b> R${valor:.2f}<br><b>Email:</b> {email}")
        info_label.setStyleSheet("font-size: 14px; text-align: center;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        # Exibir QR Code
        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if qr_code_base64:
            try:
                # Remove prefixo caso exista ("data:image/png;base64,")
                if qr_code_base64.startswith("data:image"):
                    qr_code_base64 = qr_code_base64.split(",")[1]

                # Decodifica a imagem Base64
                qr_bytes = base64.b64decode(qr_code_base64)

                # Carrega o QPixmap diretamente dos bytes decodificados
                pixmap = QPixmap()
                if not pixmap.loadFromData(qr_bytes):
                    raise ValueError("Erro ao carregar imagem do QR Code.")
                qr_label.setPixmap(pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio))
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Falha ao carregar QR Code: {str(e)}")
                qr_label.setText("⚠️ Erro ao exibir QR Code.")
        else:
            qr_label.setText("⚠️ QR Code não encontrado na resposta da API.")

        layout.addWidget(qr_label)

        # Exibir código PIX em texto (para copiar manualmente)
        pix_label = QLabel(f"<b>Código PIX:</b><br>{qr_text or 'Não informado'}")
        pix_label.setStyleSheet("font-size: 12px; text-align: center;")
        pix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pix_label)

        # Botão para voltar
        self.btn_voltar = QPushButton("Voltar ao menu")
        layout.addWidget(self.btn_voltar)

        self.setLayout(layout)
