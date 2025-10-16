import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QFont 
from PyQt6.QtCore import Qt

# Importa a classe com a lógica do nosso jogo
from logica_caca_niquel import SlotMachine

class JanelaCacaNiquel(QWidget):
  def __init__(self):
    super().__init__()
    
    # 1. Instancia a Lógica do Jogo
    self.jogo = SlotMachine(saldo_inicial=100)
    self.aposta_atual = 0 # Aposta inicial padrão

    # 2. Configura a Janela Principal (com o seu novo tamanho)
    self.setWindowTitle("UnifaBet Roulette")
    self.setGeometry(100, 100, 700, 700) # (x, y, largura, altura)
    
    # --- Vamos construir a UI em código ---
    # Definindo fontes maiores para a nova janela
    fonte_titulo = QFont("Arial", 36, QFont.Weight.Bold)
    fonte_rolos = QFont("Courier New", 90, QFont.Weight.Bold)
    fonte_normal = QFont("Arial", 16)
    fonte_botoes = QFont("Arial", 14, QFont.Weight.Bold)

    # Título
    self.label_titulo = QLabel("UnifaBET Roulette", self)
    self.label_titulo.setFont(fonte_titulo)
    self.label_titulo.setGeometry(0, 20, 700, 60) # Largura ajustada para 700
    self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Rolos (maiores e mais espaçados)
    self.label_rolo1 = QLabel("7", self)
    self.label_rolo1.setFont(fonte_rolos)
    self.label_rolo1.setGeometry(85, 120, 150, 180) # Posição e tamanho ajustados
    self.label_rolo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.label_rolo1.setStyleSheet("border: 5px solid gold; background-color: white; border-radius: 15px;")

    self.label_rolo2 = QLabel("7", self)
    self.label_rolo2.setFont(fonte_rolos)
    self.label_rolo2.setGeometry(275, 120, 150, 180) # Posição e tamanho ajustados
    self.label_rolo2.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.label_rolo2.setStyleSheet("border: 5px solid gold; background-color: white; border-radius: 15px;")

    self.label_rolo3 = QLabel("7", self)
    self.label_rolo3.setFont(fonte_rolos)
    self.label_rolo3.setGeometry(465, 120, 150, 180) # Posição e tamanho ajustados
    self.label_rolo3.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.label_rolo3.setStyleSheet("border: 5px solid gold; background-color: white; border-radius: 15px;")

    # Display de Mensagens
    self.label_mensagens = QLabel("Bem-vindo! Faça sua aposta.", self)
    self.label_mensagens.setFont(fonte_normal)
    self.label_mensagens.setGeometry(50, 340, 600, 40) # Posição e tamanho ajustados
    self.label_mensagens.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.label_mensagens.setStyleSheet("color: white; background-color: #333; border-radius: 10px;")

    # Displays de Saldo
    self.display_saldo = QLabel(f"SALDO: R${self.jogo.saldo:.2f}", self)
    self.display_saldo.setFont(fonte_normal)
    self.display_saldo.setGeometry(100, 420, 200, 40) # Posição ajustada
    self.display_saldo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Aposta
    self.display_aposta = QLabel(f"APOSTA: R${self.aposta_atual:.2f}", self)
    self.display_aposta.setFont(fonte_normal)
    self.display_aposta.setGeometry(400, 420, 200, 40) # Posição ajustada
    self.display_aposta.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Botões de Aposta menos
    self.botao_diminuir_aposta = QPushButton("-", self)
    self.botao_diminuir_aposta.setFont(fonte_botoes)
    self.botao_diminuir_aposta.setGeometry(450, 470, 50, 50)

    # aposta mais
    self.botao_aumentar_aposta = QPushButton("+", self)
    self.botao_aumentar_aposta.setFont(fonte_botoes)
    self.botao_aumentar_aposta.setGeometry(510, 470, 50, 50)

    #botao principal
    self.botao_girar = QPushButton("GIRAR", self)
    self.botao_girar.setFont(QFont('Arial', 22, QFont.Weight.Bold))
    self.botao_girar.setGeometry(200, 550, 300, 80) # Posição e tamanho ajustados
    self.botao_girar.setStyleSheet("""
      QPushButton {
        background-color: #091fe6;
        color: white;
        border-radius: 40px;
        border: 3px solid black;
      }
      QPushButton:hover { background-color: #3347F4; }
      QPushButton:pressed { background-color: #0965E6; }
    """)

    # 3. CONEXÃO DOS SINAIS E SLOTS (AGORA O JOGO FUNCIONA!)
    self.botao_girar.clicked.connect(self.executar_giro)
    self.botao_aumentar_aposta.clicked.connect(self.aumentar_aposta)
    self.botao_diminuir_aposta.clicked.connect(self.diminuir_aposta)

    # 4. Inicializa a tela com os valores iniciais
    self.atualizar_displays()

  def atualizar_displays(self):
    self.display_saldo.setText(f"SALDO: R$:{self.jogo.saldo:.2f}")
    self.display_aposta.setText(f"APOSTA: R${self.aposta_atual:.2f}")

  
  def aumentar_aposta(self):
    if self.aposta_atual < self.jogo.saldo:
      self.aposta_atual += 5
      
      self.atualizar_displays()

  
  def diminuir_aposta(self):
    if self.aposta_atual > 5:
      self.aposta_atual -= 5
    else:
      self.aposta_atual = 5

    self.atualizar_displays()


  def executar_giro(self):
    sucesso, msg = self.jogo.definir_aposta(self.aposta_atual)
    if not sucesso: 
      self.label_mensagens.setText(msg)
      return
    
    resultados, premio, msg_resultado = self.jogo.girar()

    if resultados: 
      self.label_rolo1.setText(resultados[0])
      self.label_rolo2.setText(resultados[1])
      self.label_rolo3.setText(resultados[2])

    self.label_mensagens.setText(msg_resultado)
    self.atualizar_displays()

#execução
if __name__ == '__main__':
  app = QApplication(sys.argv)
  janela = JanelaCacaNiquel()
  janela.show()
  sys.exit(app.exec())