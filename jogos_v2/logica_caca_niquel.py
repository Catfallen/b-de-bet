import random

class SlotMachine:
  """
  Esta classe gerencia toda a lógica e estado do jogo Caça-Níquel.
  """
  def __init__(self, saldo_inicial=100):
    # --- Configurações do Jogo ---
    # Define os símbolos e suas chances (pesos). Símbolos com maior peso aparecerão com mais frequência. A soma dos pesos é 100.
    #self.simbolos = ['Cereja', 'Limão', 'Laranja', 'Sino', 'BAR','7️⃣']
    self.simbolos = ['🍒', '🍋', '🍊', '🔔', '🍫', '7️⃣']
    self.pesos = [30,25,20,15,7,3]

    # --- Estado do Jogo (variáveis que mudam durante o jogo) ---
    self.saldo = saldo_inicial
    self.aposta_atual = 0

  
  def definir_aposta(self, valor):
    """
    Valida e define o valor da aposta para o próximo giro.
    Retorna uma tupla: (True/False se foi sucesso, "Mensagem para o usuário").
    """
    try: 
      valor_aposta = float(valor)

      if valor_aposta <= 0:
        return False, 'A aposta deve ser maior que zero'
      if valor_aposta > self.saldo:
        return False, 'Saldo insuficiente para está aposta!'
      
      self.aposta_atual = valor_aposta
      return True, f"Aposta de ${valor_aposta} definida."
    
    except (ValueError, TypeError):
      return False, 'Valor da aposta inválido. Use somente números'
    

  def girar(self):
    """
    Executa um giro da máquina.
    1. Verifica se uma aposta válida foi definida.
    2. Subtrai o valor da aposta do saldo.
    3. Gera os 3 resultados aleatórios com base nos pesos.
    4. Calcula o prêmio com base nos resultados.
    5. Adiciona o prêmio ao saldo.
    Retorna os resultados, o prêmio e uma mensagem.
    """
    if self.aposta_atual <= 0:
      return None, 0, "Defina um valor de aposta primeiro!"
    if self.aposta_atual > self.saldo:
      return None, 0, "Saldo insuficiente para girar!"
    
    # 2. Registrar saldo antes do giro (para debug)
    saldo_inicial = self.saldo

    # 3. Processar o giro
    self.saldo -= self.aposta_atual
    resultados = random.choices(self.simbolos,weights=self.pesos, k=3)
    premio = self._calcular_premio(resultados)
    self.saldo += premio

    # 4. Mensagem
    multiplicador = premio / self.aposta_atual

    if multiplicador >= 100:      # Três 7️⃣
      mensagem = f"🔥 MEGA JACKPOT! 100x → ${premio}!"
    elif multiplicador >= 50:     # Três BAR
      mensagem = f"🎉 JACKPOT! 50x → ${premio}!"
    elif multiplicador >= 20:     # Três Sino
      mensagem = f"🎊 GRANDE PRÊMIO! 20x → ${premio}!"
    elif multiplicador >= 10:     # Três Laranja
      mensagem = f"⭐ BOA! 10x → ${premio}!"
    elif multiplicador >= 5:      # Três Limão
      mensagem = f"👍 GANHOU! 5x → ${premio}!"
    elif multiplicador >= 3:      # Três Cereja
      mensagem = f"👏 CERTO! 3x → ${premio}!"
    elif multiplicador >= 1:      # Duas Cerejas
      mensagem = f"✅ Recuperou a aposta! ${premio}"
    else:                         # Sem prêmio
      mensagem = "😅 Tente novamente!"

    return resultados,premio, mensagem
  

  def _calcular_premio(self, resultados):
    #Lógica interna e privada para calcular os prêmios.

    if resultados[0] == resultados[1] == resultados[2]:
      simbolo = resultados[0]
      
      # if simbolo == '7️⃣': return self.aposta_atual * 100
      # if simbolo == 'BAR': return self.aposta_atual * 50
      # if simbolo == 'Sino': return self.aposta_atual * 20
      # if simbolo == 'Laranja': return self.aposta_atual * 10
      # if simbolo == 'Limão': return self.aposta_atual * 5
      # if simbolo == 'Cereja': return self.aposta_atual * 3

      if simbolo == '7️⃣': return self.aposta_atual * 100
      if simbolo == '🍫': return self.aposta_atual * 50
      if simbolo == '🔔': return self.aposta_atual * 20
      if simbolo == '🍊': return self.aposta_atual * 10
      if simbolo == '🍋': return self.aposta_atual * 5
      if simbolo == '🍒': return self.aposta_atual * 1

    #checar 2 cerejas
    if resultados.count('🍒') == 2:
      return self.aposta_atual * 1 #devolve a aposta para engajar
  
    return 0
  

# --- Bloco de Teste ---
# Este código só executa quando você roda ESTE arquivo diretamente.
# Ele serve para testar a classe SlotMachine de forma isolada.
if __name__ == '__main__':
  print("--- INICIANDO TESTE DA LÓGICA DO JOGO ---")
  print('-'*50)

  jogo_teste = SlotMachine(saldo_inicial=50)
  print(f'Saldo inicial: {jogo_teste.saldo}')

  # Teste 1: Definir uma aposta válida
  sucesso, msg = jogo_teste.definir_aposta(10)
  print(f"Tentando aposta de R$10...Resultado {msg}")

  # Teste 2: Simular um giro
  print("\nGirando a roleta...")
  resultados, premio, msg_resultado = jogo_teste.girar()
  if resultados:
    print(f'Resultados {resultados}')
    print(f'Mensagens {msg_resultado}')
    print(f'Saldo Final {jogo_teste.saldo:.2f}')

  # teste 3: resultado inválido
  print('\n')
  sucesso, msg = jogo_teste.definir_aposta(1000)
  print(f"Tentando aposta de R$1000...Resultado {msg}")
  print(f"Saldo continua {jogo_teste.saldo:.2f}")

  print("\n--- TESTE CONCLUÍDO ---")