import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, 
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
    QSpinBox, QDoubleSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

class MinesGame(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Configurações do Jogo ---
        self.GRID_SIZE = 5
        self.game_in_progress = False
        self.mines_positions = set()
        self.revealed_gems = 0
        self.current_bet = 0.10
        self.num_mines = 2
        
        self.setWindowTitle("Jogo de Minas (PyQt)")
        self.setGeometry(100, 100, 400, 500)

        # Widget central e layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- 1. Painel de Informações ---
        info_layout = QHBoxLayout()
        self.multiplier_label = QLabel("Multiplicador: 1.00x")
        self.winnings_label = QLabel("Prêmio: R$ 0.00")
        info_layout.addWidget(self.multiplier_label)
        info_layout.addWidget(self.winnings_label)
        main_layout.addLayout(info_layout)

        # --- 2. Grade do Jogo ---
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.buttons = []
        self.init_grid()
        main_layout.addLayout(self.grid_layout)

        # --- 3. Painel de Controles ---
        controls_layout = QGridLayout()
        
        # Aposta
        controls_layout.addWidget(QLabel("Quantia (R$):"), 0, 0)
        self.bet_input = QDoubleSpinBox()
        self.bet_input.setMinimum(0.10)
        self.bet_input.setMaximum(100.0)
        self.bet_input.setSingleStep(0.1)
        self.bet_input.setValue(0.10)
        controls_layout.addWidget(self.bet_input, 0, 1)

        # Minas
        controls_layout.addWidget(QLabel("Número de Minas:"), 1, 0)
        self.mines_input = QSpinBox()
        self.mines_input.setMinimum(1)
        # O máximo de minas não pode ser maior que o total de células - 1
        self.mines_input.setMaximum(self.GRID_SIZE * self.GRID_SIZE - 1)
        self.mines_input.setValue(2)
        controls_layout.addWidget(self.mines_input, 1, 1)

        # Botão de Iniciar Jogo
        self.start_button = QPushButton("Começar o Jogo")
        self.start_button.clicked.connect(self.start_game)
        controls_layout.addWidget(self.start_button, 2, 0, 1, 2)
        
        # Botão de Retirar
        self.cashout_button = QPushButton("Retirar Ganhos")
        self.cashout_button.clicked.connect(self.cash_out)
        self.cashout_button.setEnabled(False) # Desabilitado no início
        controls_layout.addWidget(self.cashout_button, 3, 0, 1, 2)
        
        main_layout.addLayout(controls_layout)

    def init_grid(self):
        """Cria a grade de botões inicial."""
        self.buttons = []
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                button = QPushButton()
                button.setFixedSize(60, 60)
                button.setFont(QFont("Arial", 16))
                button.setEnabled(False) # Botões desabilitados até o jogo começar
                # Conecta o clique a uma função, passando a posição do botão
                button.clicked.connect(lambda _, r=row, c=col: self.grid_button_clicked(r, c))
                self.grid_layout.addWidget(button, row, col)
                self.buttons.append(button)

    def start_game(self):
        """Prepara e inicia uma nova rodada do jogo."""
        self.current_bet = self.bet_input.value()
        self.num_mines = self.mines_input.value()
        self.game_in_progress = True
        self.revealed_gems = 0
        
        # Resetar a aparência da grade
        for i, button in enumerate(self.buttons):
            button.setEnabled(True)
            button.setText("")
            button.setStyleSheet("") # Limpa estilos
            
        # Colocar as minas aleatoriamente
        self.place_mines()
        
        # Atualizar a interface
        self.update_display()
        self.start_button.setText("Jogo em Andamento")
        self.start_button.setEnabled(False)
        self.cashout_button.setEnabled(False) # Habilitado após o primeiro acerto
        self.bet_input.setEnabled(False)
        self.mines_input.setEnabled(False)

    def place_mines(self):
        """Define as posições das minas de forma aleatória na grade."""
        total_cells = self.GRID_SIZE * self.GRID_SIZE
        all_positions = list(range(total_cells))
        mine_indices = random.sample(all_positions, self.num_mines)
        self.mines_positions = set(mine_indices)

    def grid_button_clicked(self, row, col):
        """Chamado quando um botão da grade é clicado."""
        if not self.game_in_progress:
            return
            
        index = row * self.GRID_SIZE + col
        button = self.buttons[index]
        
        if not button.isEnabled(): # Se já foi clicado
            return

        if index in self.mines_positions:
            # Fim de jogo - acertou uma mina
            button.setText("💣")
            button.setStyleSheet("background-color: #ff4d4d; color: white;")
            self.game_over(won=False)
        else:
            # Acertou um diamante
            button.setText("💎")
            button.setStyleSheet("background-color: #4CAF50; color: white;")
            button.setEnabled(False) # Desabilita o botão após o clique
            self.revealed_gems += 1
            self.cashout_button.setEnabled(True) # Permite retirar os ganhos
            self.update_display()

            # Verifica se o jogador encontrou todos os diamantes
            total_gems = (self.GRID_SIZE * self.GRID_SIZE) - self.num_mines
            if self.revealed_gems == total_gems:
                self.game_over(won=True)

    def calculate_multiplier(self):
        """Calcula o multiplicador com base nos diamantes encontrados."""
        if self.revealed_gems == 0:
            return 1.0
        
        # Fórmula de exemplo simples para o multiplicador
        # Pode ser substituída por uma lógica mais complexa
        total_cells = self.GRID_SIZE * self.GRID_SIZE
        p_safe = (total_cells - self.num_mines) / total_cells
        multiplier = (1 / p_safe) ** self.revealed_gems
        return round(multiplier, 2)

    def update_display(self):
        """Atualiza os rótulos de multiplicador e prêmio."""
        multiplier = self.calculate_multiplier()
        winnings = self.current_bet * multiplier
        
        self.multiplier_label.setText(f"Multiplicador: {multiplier:.2f}x")
        self.winnings_label.setText(f"Prêmio: R$ {winnings:.2f}")

    def game_over(self, won):
        """Finaliza o jogo, seja por vitória ou derrota."""
        self.game_in_progress = False
        self.reveal_all_mines()
        
        if won:
            message = f"Você encontrou todos os diamantes! Ganhou R$ {self.winnings_label.text().split(' ')[-1]}!"
        else:
            message = "Você acertou uma mina! Fim de jogo."

        QMessageBox.information(self, "Fim de Jogo", message)
        self.reset_ui_for_new_game()

    def cash_out(self):
        """Permite que o jogador retire os ganhos atuais."""
        if not self.game_in_progress or self.revealed_gems == 0:
            return
            
        self.game_in_progress = False
        winnings_value = self.current_bet * self.calculate_multiplier()
        QMessageBox.information(self, "Ganhos Retirados", f"Você ganhou R$ {winnings_value:.2f}!")
        self.reveal_all_mines()
        self.reset_ui_for_new_game()

    def reveal_all_mines(self):
        """Mostra a posição de todas as minas no final da rodada."""
        for i, button in enumerate(self.buttons):
            button.setEnabled(False) # Desabilita todos
            if i in self.mines_positions and not button.text():
                button.setText("💣")
                button.setStyleSheet("background-color: #cccccc;")

    def reset_ui_for_new_game(self):
        """Reseta a interface para permitir um novo jogo."""
        self.start_button.setText("Começar o Jogo")
        self.start_button.setEnabled(True)
        self.cashout_button.setEnabled(False)
        self.bet_input.setEnabled(True)
        self.mines_input.setEnabled(True)
        self.multiplier_label.setText("Multiplicador: 1.00x")
        self.winnings_label.setText("Prêmio: R$ 0.00")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MinesGame()
    window.show()
    sys.exit(app.exec())