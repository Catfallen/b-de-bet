import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QListWidget, QListWidgetItem,
    QApplication
)
from PyQt6.QtCore import Qt
from roleta import JanelaPrincipal
from caca_niquel import JanelaCacaNiquel
from mines import MinesGame
class MenuWindow(QWidget):
    def __init__(self, token=""):
        super().__init__()
        self.token = token
        self.setWindowTitle("Menu Principal - B de Bet")
        self.setFixedSize(400, 500)

        self.setup_ui()

    def setup_ui(self):
        layout_principal = QVBoxLayout()

        # ======== TOPO ========
        topo_layout = QHBoxLayout()

        self.lbl_saldo = QLabel("Saldo: R$ 0,00")
        self.lbl_saldo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        topo_layout.addWidget(self.lbl_saldo)

        btn_saldo = QPushButton("🔄 Atualizar saldo")
        btn_saldo.clicked.connect(self.atualizar_saldo)
        topo_layout.addWidget(btn_saldo)

        btn_depositar = QPushButton("💰 Depositar")
        btn_depositar.clicked.connect(self.depositar)
        topo_layout.addWidget(btn_depositar)

        layout_principal.addLayout(topo_layout)

        # ======== MEIO ========
        lbl_jogos = QLabel("🎮 Jogos disponíveis:")
        lbl_jogos.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(lbl_jogos)

        self.lista_jogos = QListWidget()
        for jogo in ["Mines", "Roleta", "Caça Níquel"]:
            item = QListWidgetItem(jogo)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lista_jogos.addItem(item)
        self.lista_jogos.itemClicked.connect(self.abrir_jogo)
        layout_principal.addWidget(self.lista_jogos)

        # ======== RODAPÉ ========
        btn_menu = QPushButton("🏠 Menu Principal")
        btn_menu.clicked.connect(self.voltar_menu)
        layout_principal.addWidget(btn_menu)

        self.setLayout(layout_principal)

        # Carrega saldo inicial
        self.atualizar_saldo()

    # ==========================
    # Funções
    # ==========================

    def atualizar_saldo(self):
        """Consulta o saldo atual do usuário"""
        try:
            url = "http://localhost:3000/payments/saldo"
            headers = {"Authorization": f"Bearer {self.token}"} 
            r = requests.post(url, headers=headers)

            if r.status_code == 200:
                data = r.json()
                saldo_str = data.get("saldo", "0")

                try:
                    saldo = float(saldo_str)
                except ValueError:
                    saldo = 0.0

                self.lbl_saldo.setText(f"Saldo: R$ {saldo:.2f}")
            else:
                QMessageBox.warning(self, "Erro", f"Não foi possível obter o saldo.\n{r.text}")

        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erro", "Não foi possível conectar ao servidor (localhost:3000).")
    def depositar(self):
        from deposito import DepositoWindow
        self.deposito_window = DepositoWindow(self.token)
        self.deposito_window.show()

    def abrir_jogo(self, item):
        """Abre o jogo selecionado"""
        jogo = item.text()
        
        if jogo == "Roleta":
            try:
            # Executa o script roleta.py em um novo processo Python
                self.roleta_window = JanelaPrincipal(token=self.token)
                self.roleta_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao abrir o jogo Roleta:\n{e}")
        elif jogo == "Caça Níquel":
            try:
                self.caca_window = JanelaCacaNiquel()
                self.caca_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao abrir o jogo Caça níquel:\n{e}")
        elif jogo == "Mines":
            try:
                self.mines_window = MinesGame()
                self.mines_window.show()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao abrir o jogo Mines:\n{e}")
            
    def voltar_menu(self):
        """Retorna ao menu principal"""
        QMessageBox.information(self, "Menu", "Você já está no menu principal 😎")
