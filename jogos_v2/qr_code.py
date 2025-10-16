import base64
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class QrCodeWindow(QWidget):
    def __init__(self, qr_text: str, qr_payload: str, valor: float = 0, email: str = ""):
        super().__init__()
        self.setWindowTitle("Leitura do QR Code")
        self.setGeometry(100, 100, 350, 400)

        layout = QVBoxLayout()

        # Exibe informações básicas
        try:
            valor_float = float(valor)
        except (ValueError, TypeError):
            valor_float = 0.0
        
        info_label = QLabel(f"<b>Depósito:</b> R${valor_float:.2f}<br><b>Email:</b> {email}")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        # Exibir QR Code
        qr_label = QLabel()
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if qr_payload:
            try:
                if qr_payload.startswith("data:image"):
                    qr_payload = qr_payload.split(",")[1]
                qr_bytes = base64.b64decode(qr_payload)
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

        # Exibir código PIX em texto
        pix_label = QLabel(f"<b>Código PIX:</b><br>{qr_text or 'Não informado'}")
        pix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(pix_label)

        # Botão para voltar
        self.btn_voltar = QPushButton("Voltar ao menu")
        layout.addWidget(self.btn_voltar)

        self.setLayout(layout)
