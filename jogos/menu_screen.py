# menu_screen.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
from mines import MinesGame  # importa o jogo Mines

class MenuScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Menu Principal - Selecione o Jogo"))

        self.games_list = QListWidget()
        self.games_list.addItems(["💣 Mines", "🚀 Crash", "🎰 Slot"])
        layout.addWidget(self.games_list)

        btn_play = QPushButton("Jogar")
        btn_play.clicked.connect(self.play_game)
        layout.addWidget(btn_play)

        self.setLayout(layout)

    def play_game(self):
        game = self.games_list.currentItem()
        if game:
            if game.text() == "💣 Mines":
                self.mines_window = MinesGame()  # abre o Mines
                self.mines_window.show()
            else:
                QMessageBox.information(self, "Jogo selecionado", f"Você selecionou {game.text()}")
        else:
            QMessageBox.warning(self, "Erro", "Selecione um jogo primeiro.")
