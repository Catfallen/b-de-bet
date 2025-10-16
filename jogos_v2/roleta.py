from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt 
import random
from saldo import getSaldo
# A classe principal da aplicação, herda de QMainWindow
class JanelaPrincipal(QMainWindow):
    def __init__(self,token):
        super().__init__()

        # --- Configuração Básica da Janela ---
        self.setWindowTitle("🎡 Jogo Double - Dia das Crianças")
        self.setFixedSize(450, 550) # Tamanho fixo da janela

        # --- Variáveis de Estado do Jogo (Back-end) ---
        self.token = token
        self.saldo = getSaldo(self.token)            # Saldo inicial do jogador
        self.aposta = 0             # Valor da aposta atual
        self.escolha_jogador = None # Armazena a cor escolhida ('vermelho', 'preto', 'branco')
        self.girando = False        # Flag para evitar múltiplos giros simultâneos

        self.historico_jogadas = [] # Lista para armazenar os resultados (cores)
        self.max_historico = 16     # Limite de resultados mostrados no histórico

        # --- Componentes da Interface (Widgets) ---
        
        # 1. Label principal para mensagens e saldo
        self.label = QLabel(f"Escolha uma cor, defina a aposta e gire! Saldo: {self.saldo} fichas", self)
        self.label.setStyleSheet("font-size: 16px; text-align: center; margin-bottom: 20px;")

        # 2. Widgets do Histórico
        self.historico_label = QLabel("Histórico das Últimas Jogadas:")
        self.historico_display = QLabel("Nenhuma jogada ainda.")
        self.historico_display.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;")
        self.historico_display.setWordWrap(True) # Permite quebra de linha

        # 3. Quadrado que exibe o resultado da roleta/animação
        self.quadrado = QLabel(self)
        self.quadrado.setFixedSize(80, 80)
        self.quadrado.setStyleSheet("background-color: gray; border: 4px solid black; border-radius: 10px;")

        # 4. Campo de Aposta (Input e Label)
        self.aposta_label = QLabel("Valor da Aposta:")
        self.aposta_input = QLineEdit()
        self.aposta_input.setPlaceholderText("Digite o valor (ex: 10)")
        self.aposta_input.setText("10") # Valor padrão
        self.aposta_input.setFixedSize(100, 30)
        
        # Layout horizontal para organizar o campo de aposta e seu rótulo
        aposta_layout = QHBoxLayout()
        aposta_layout.addWidget(self.aposta_label)
        aposta_layout.addWidget(self.aposta_input)
        aposta_layout.addStretch() # Empurra os widgets para a esquerda

        # 5. Botões de Escolha e Giro
        self.botao_vermelho = QPushButton("🔴 Vermelho (x2)")
        self.botao_preto = QPushButton("⚫ Preto (x2)")
        self.botao_branco = QPushButton("⚪ Branco (x14)")
        self.botao_girar = QPushButton("🎲 GIRAR")

        # Estilos dos botões
        self.botao_vermelho.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        self.botao_preto.setStyleSheet("background-color: #34495e; color: white; padding: 10px;")
        self.botao_branco.setStyleSheet("background-color: white; color: black; padding: 10px; border: 1px solid black;")
        self.botao_girar.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold; padding: 15px;")


        # --- Lógica da Animação da Roleta ---
        # Sequência de cores para a animação (10 cores no total: 5 vermelhos, 5 pretos, 1 branco)
        self.cores_roleta = ["vermelho", "preto"] * 5 + ["branco"] 
        self.indice_atual = 0       # Índice atual na sequência de cores para a animação
        self.passos_restantes = 0   # Contador de ticks para o fim da animação
        self.resultado_final = None # Cor sorteada para o resultado

        self.timer = QTimer()
        self.timer.setInterval(50) # Intervalo inicial do timer (50ms)
        self.timer.timeout.connect(self.animar_quadrado) # Conecta ao método de animação

        # --- Organização do Layout Principal ---
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        
        # Adiciona Histórico
        layout.addWidget(self.historico_label)
        layout.addWidget(self.historico_display) 
        layout.addSpacing(15)

        # Adiciona Quadrado (Resultado/Animação)
        # Usa Alinhamento Centralizado para o quadrado
        layout.addWidget(self.quadrado, alignment=Qt.AlignmentFlag.AlignCenter) 
        layout.addSpacing(20)
        
        # Adiciona Campo de Aposta
        layout.addLayout(aposta_layout)
        layout.addSpacing(10)
        
        # Adiciona Botões de Escolha
        layout.addWidget(self.botao_vermelho)
        layout.addWidget(self.botao_preto)
        layout.addWidget(self.botao_branco)
        layout.addSpacing(20)
        
        # Adiciona Botão de Giro
        layout.addWidget(self.botao_girar)

        # Define o container central para o layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # --- Conexão de Sinais/Eventos (Clique dos Botões) ---
        self.botao_vermelho.clicked.connect(lambda: self.selecionar_cor("vermelho"))
        self.botao_preto.clicked.connect(lambda: self.selecionar_cor("preto"))
        self.botao_branco.clicked.connect(lambda: self.selecionar_cor("branco"))
        self.botao_girar.clicked.connect(self.girar_roleta)

    # Função auxiliar: Mapeia a string da cor para o código hexadecimal CSS
    def _cor_para_css(self, cor):
        if cor == "vermelho":
            return "#e74c3c"
        elif cor == "preto":
            return "#34495e"
        elif cor == "branco":
            return "white"
        return "gray" # Cor padrão, caso não encontre
    
    # Função que atualiza a exibição do histórico de jogadas
    def _atualizar_historico_display(self):
        # Remove o mais antigo se exceder o limite
        while len(self.historico_jogadas) > self.max_historico:
            self.historico_jogadas.pop(0)
        
        display_text = ""
        # Converte as cores para emojis para exibição
        for cor in self.historico_jogadas:
            if cor == "vermelho":
                emoji = "🔴"
            elif cor == "preto":
                emoji = "⚫"
            elif cor == "branco":
                emoji = "⚪"
            else:
                emoji = "❓"

            # Adiciona o emoji com um pequeno estilo HTML/CSS para espaçamento
            display_text += f'<span style="font-size: 18px; margin-right: 5px;">{emoji}</span>'

        # Atualiza o QLabel com a string de emojis
        if not display_text:
            self.historico_display.setText("Nenhuma jogada ainda.")
        else:
            self.historico_display.setText(display_text)

    # Método chamado ao clicar nos botões Vermelho, Preto ou Branco
    def selecionar_cor(self, cor):
        if self.girando:
            self.label.setText("Aguarde o fim do giro!")
            return
        self.escolha_jogador = cor
        self.label.setText(f"Você escolheu {cor}. Defina sua aposta e clique em 'GIRAR'. Saldo: {self.saldo} fichas")
        
        # Destaca o botão da cor selecionada
        for btn, c in zip([self.botao_vermelho, self.botao_preto, self.botao_branco], ["vermelho", "preto", "branco"]):
            style = ""
            if c == cor:
                # Estilo de destaque (borda amarela)
                style = f"background-color: {self._cor_para_css(c)}; color: yellow; font-weight: bold; border: 3px solid yellow; padding: 10px;"
            else:
                # Estilo padrão
                style = f"background-color: {self._cor_para_css(c)}; color: {'black' if c == 'branco' else 'white'}; padding: 10px; {'border: 1px solid black;' if c == 'branco' else ''}"
            btn.setStyleSheet(style)


    # Método chamado ao clicar no botão GIRAR
    def girar_roleta(self):
        if self.girando:
            return
        if not self.escolha_jogador:
            self.label.setText("Escolha uma cor primeiro!")
            return
    
    # 1. Validação da aposta
        try:
            self.aposta = int(self.aposta_input.text())
            if self.aposta <= 0:
                self.label.setText("A aposta deve ser positiva!")
                return
        except ValueError:
            self.label.setText("Digite um número válido para a aposta!")
            return

    # 2. Validação de saldo
        if self.saldo < self.aposta:
            self.label.setText(f"Saldo insuficiente! Saldo: {self.saldo}")
            return

    # 3. Início do giro
        self.girando = True
        self.saldo -= self.aposta
        self.label.setText(f"Girando roleta... Aposta: {self.aposta} | Saldo: {self.saldo}")

    # Desabilita botões e input
        self.botao_vermelho.setEnabled(False)
        self.botao_preto.setEnabled(False)
        self.botao_branco.setEnabled(False)
        self.botao_girar.setEnabled(False)
        self.aposta_input.setEnabled(False)

    # 4. Chamada à API
        import requests
        url = "http://localhost:3000/bet/apostar/roleta"
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"valor": self.aposta, "cor": self.escolha_jogador}

        try:
            r = requests.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                dados = r.json()
                print(dados)
            # Resultado vindo do servidor
                self.resultado_final = dados.get("corAleatoria", "gray")
                self.ganho_total = dados.get("valor", 0)
                self.resultado_bool = dados.get("resultado", False)
            else:
                self.resultado_final = "gray"
                self.ganho_total = 0
                self.resultado_bool = False
                print("Erro API:", r.text)
        except Exception as e:
            self.resultado_final = "gray"
            self.ganho_total = 0
            self.resultado_bool = False
            print("Erro ao chamar API:", e)

    # 5. Configuração da animação
        self.passos_restantes = 20
        self.timer.setInterval(80)
        self.timer.start()
    # Método chamado repetidamente pelo QTimer para criar a animação
    def animar_quadrado(self):
        # Enquanto houver mais de 1 passo restante, continua a animação rápida
        if self.passos_restantes > 1:
            # Seleciona a próxima cor da sequência de animação
            cor_animacao = self.cores_roleta[self.indice_atual % len(self.cores_roleta)]
            css_color = self._cor_para_css(cor_animacao)
            self.quadrado.setStyleSheet(f"background-color: {css_color}; border: 4px solid black; border-radius: 10px;")
            self.indice_atual += 1

        self.passos_restantes -= 1
        
        # Condição de parada: Fim da animação
        if self.passos_restantes <= 0:
            self.timer.stop()
            self.parar_roleta()
            return
        
        # Desaceleração: Aumenta o intervalo do timer nos últimos 5 passos
        if self.passos_restantes < 5:
            # Aumenta o intervalo gradativamente (80 + 4*100 = 480ms, 80 + 1*100 = 180ms)
            novo_intervalo = 80 + (5 - self.passos_restantes) * 100 
            self.timer.setInterval(novo_intervalo)

        
    # Método chamado após a animação para definir o resultado e pagar prêmios
    def parar_roleta(self):
        self.girando = False
        
        # 1. Aplica o estilo FINAL do resultado no quadrado
        cor_final_css = self._cor_para_css(self.resultado_final)
        # Borda especial para o branco (para destacá-lo)
        border_color = 'gold' if self.resultado_final == 'branco' else 'white'
        self.quadrado.setStyleSheet(f"background-color: {cor_final_css}; border: 4px solid {border_color}; border-radius: 10px;")

        # 2. Atualiza o Histórico
        self.historico_jogadas.append(self.resultado_final)
        self._atualizar_historico_display()

        # 3. Lógica de Pagamento
        ganho_total = 0 
        mensagem = f"Resultado: {self.resultado_final}. "
        
        
        if self.escolha_jogador == self.resultado_final:
            if self.resultado_final == "branco":
                ganho_multiplicador = 14
                ganho_total = self.aposta * ganho_multiplicador 
                mensagem += f"💥 BRANCO! Você ganhou {ganho_total} fichas!"
            else: 
                ganho_multiplicador = 2
                # O prêmio é o valor apostado * 2 (lucro = valor apostado)
                ganho_total = self.aposta * ganho_multiplicador
                mensagem += f"🎉 Você ganhou {ganho_total} fichas!"
        else:
            # O jogador perdeu a aposta (já foi deduzida no início do giro)
            mensagem += f"😢 Você perdeu {self.aposta} fichas."

        self.saldo += ganho_total # Adiciona o ganho total (se houver) ao saldo
        
        # 4. Finaliza e Restaura Controles
        self.label.setText(f"{mensagem} Saldo: {self.saldo} fichas")
        self.escolha_jogador = None # Reseta a escolha do jogador

        # Reabilita os botões e o campo de aposta
        self.botao_vermelho.setEnabled(True)
        self.botao_preto.setEnabled(True)
        self.botao_branco.setEnabled(True)
        self.botao_girar.setEnabled(True)
        self.aposta_input.setEnabled(True) 

        # Restaura o estilo dos botões de cor
        for btn, c in zip([self.botao_vermelho, self.botao_preto, self.botao_branco], ["vermelho", "preto", "branco"]):
            btn.setStyleSheet(f"background-color: {self._cor_para_css(c)}; color: {'black' if c == 'branco' else 'white'}; padding: 10px; {'border: 1px solid black;' if c == 'branco' else ''}")