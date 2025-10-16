# menu_screen.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
import utils
from mines import MinesGame
from deposito import DepositoWindow  # ✅ importar a tela de depósito

class MenuScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Menu Principal - Selecione o Jogo")
        self.layout.addWidget(self.label)

        # Lista de jogos
        self.games_list = QListWidget()
        self.games_list.addItems(["💣 Mines", "🚀 Crash", "🎰 Slot"])
        self.layout.addWidget(self.games_list)

        # Botão jogar
        btn_play = QPushButton("Jogar")
        btn_play.clicked.connect(self.play_game)
        self.layout.addWidget(btn_play)

        # ✅ Botão para abrir a tela de depósito
        btn_depositar = QPushButton("💰 Fazer Depósito")
        btn_depositar.clicked.connect(self.abrir_deposito)
        self.layout.addWidget(btn_depositar)

        #botão pagamentos
        
        self.setLayout(self.layout)

    def update_token_label(self):
        """Atualiza o label com o token global"""
        self.label.setText(f"Menu Principal - Token: {utils.TOKEN}")

    def play_game(self):
        game = self.games_list.currentItem()
        if game:
            if game.text() == "💣 Mines":
                self.mines_window = MinesGame()
                self.mines_window.show()
            else:
                QMessageBox.information(self, "Jogo selecionado", f"Você selecionou {game.text()}")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um jogo primeiro.")

    def abrir_deposito(self):
        """Abre a janela de depósito"""
        self.deposito_window = DepositoWindow()
        self.deposito_window.show()
