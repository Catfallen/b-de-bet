from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from deposito import DepositoWindow
from qrcode_tela import QrCodeWindow
import sys


class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("B de Bet - Menu Principal")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.btn_deposito = QPushButton("Fazer Depósito")
        self.btn_deposito.clicked.connect(self.abrir_deposito)

        layout.addWidget(self.btn_deposito)
        self.setLayout(layout)

    def abrir_deposito(self):
        self.deposito = DepositoWindow()
        self.deposito.abrir_qrcode.connect(self.abrir_qrcode_tela)
        self.deposito.show()

    def abrir_qrcode_tela(self, dados,data):
        self.qr_window = QrCodeWindow(dados,data)
        self.qr_window.btn_voltar.clicked.connect(self.qr_window.close)
        self.qr_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MenuPrincipal()
    janela.show()
    sys.exit(app.exec_())
