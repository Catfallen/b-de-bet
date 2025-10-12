import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox
)
from PyQt5.QtCore import QSize


class MinesGame(QWidget):
    def __init__(self, rows=5, cols=5):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.total_cells = rows * cols
        self.balance = 100.0
        self.bet_amount = 0.0
        self.mines = 3
        self.opened = 0
        self.multiplier = 1.0
        self.playing = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("💣 Mines com Sistema de Saldo e Odd")
        self.setFixedSize(400, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Label de saldo
        self.balance_label = QLabel(f"Saldo: R$ {self.balance:.2f}")
        self.balance_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.balance_label)

        # Entrada de aposta
        bet_layout = QHBoxLayout()
        bet_layout.addWidget(QLabel("Aposta:"))
        self.bet_input = QLineEdit()
        self.bet_input.setPlaceholderText("ex: 10")
        bet_layout.addWidget(self.bet_input)

        bet_layout.addWidget(QLabel("Minas:"))
        self.mines_input = QLineEdit()
        self.mines_input.setPlaceholderText("ex: 3")
        bet_layout.addWidget(self.mines_input)
        self.layout.addLayout(bet_layout)

        # Botões de controle
        control_layout = QHBoxLayout()
        self.play_btn = QPushButton("🎲 Jogar")
        self.play_btn.clicked.connect(self.start_game)
        control_layout.addWidget(self.play_btn)

        self.cashout_btn = QPushButton("💵 Retirar")
        self.cashout_btn.clicked.connect(self.cashout)
        self.cashout_btn.setEnabled(False)
        control_layout.addWidget(self.cashout_btn)
        self.layout.addLayout(control_layout)

        # Label de odd
        self.odd_label = QLabel("Odd: x1.00")
        self.odd_label.setStyleSheet("font-size: 16px; color: #555;")
        self.layout.addWidget(self.odd_label)

        # Grade do jogo
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)
        self.buttons = {}
        for r in range(self.rows):
            for c in range(self.cols):
                btn = QPushButton("")
                btn.setFixedSize(QSize(50, 50))
                btn.setStyleSheet("font-size: 16px;")
                btn.clicked.connect(lambda _, row=r, col=c: self.reveal(row, col))
                self.grid.addWidget(btn, r, c)
                self.buttons[(r, c)] = btn

    def start_game(self):
        if self.playing:
            QMessageBox.warning(self, "Aviso", "O jogo já está em andamento!")
            return

        try:
            self.bet_amount = float(self.bet_input.text())
            self.mines = int(self.mines_input.text())
        except ValueError:
            QMessageBox.warning(self, "Erro", "Digite valores válidos para aposta e minas.")
            return

        if self.bet_amount <= 0 or self.bet_amount > self.balance:
            QMessageBox.warning(self, "Saldo insuficiente", "Aposta inválida!")
            return

        if not (1 <= self.mines < self.total_cells):
            QMessageBox.warning(self, "Erro", "Número de minas inválido!")
            return

        self.playing = True
        self.balance -= self.bet_amount
        self.update_balance()
        self.cashout_btn.setEnabled(True)

        self.opened = 0
        self.multiplier = self.calculate_base_odd()
        self.odd_label.setText(f"Odd: x{self.multiplier:.2f}")
        self.mine_positions = set(random.sample(range(self.total_cells), self.mines))

        for btn in self.buttons.values():
            btn.setText("")
            btn.setEnabled(True)
            btn.setStyleSheet("background-color: none; font-size: 16px;")

    def calculate_base_odd(self):
        safe_cells = self.total_cells - self.mines
        probability = safe_cells / self.total_cells
        odd = (1 / probability) * 0.97
        return odd

    def reveal(self, row, col):
        if not self.playing:
            return
        index = row * self.cols + col
        btn = self.buttons[(row, col)]

        if not btn.isEnabled():
            return

        if index in self.mine_positions:
            btn.setText("💣")
            btn.setStyleSheet("background-color: red;")
            self.end_game(False)
        else:
            btn.setText("✔")
            btn.setStyleSheet("background-color: lightgreen;")
            btn.setEnabled(False)
            self.opened += 1
            self.multiplier *= 1.05  # aumenta a odd a cada acerto
            self.odd_label.setText(f"Odd: x{self.multiplier:.2f}")

    def cashout(self):
        if not self.playing:
            return
        gain = self.bet_amount * self.multiplier
        self.balance += gain
        self.update_balance()
        QMessageBox.information(self, "Retirada 💵", f"Você retirou R$ {gain:.2f}!")
        self.end_game(True)

    def end_game(self, win):
        for (r, c), btn in self.buttons.items():
            btn.setEnabled(False)
            if r * self.cols + c in self.mine_positions:
                btn.setText("💣")
                btn.setStyleSheet("background-color: #ff6666;")

        if not win:
            QMessageBox.critical(self, "💥 Perdeu", "Você clicou em uma mina! Aposta perdida.")
        self.playing = False
        self.cashout_btn.setEnabled(False)
        self.update_balance()

    def update_balance(self):
        self.balance_label.setText(f"Saldo: R$ {self.balance:.2f}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinesGame()
    window.show()
    sys.exit(app.exec_())
