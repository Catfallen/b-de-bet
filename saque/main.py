# token.py

import requests

CLIENT_ID = "Client_Id_b1bd8285aea727e40e4b645b0b1164c2150a21ec"
CLIENT_SECRET = "Client_Secret_9f1b0b1e7214107d2d3ca5cc8e2e28eaa6e621fa"


# Endpoint de autenticação
url = "https://api.efipay.com.br/identity/oauth/token"  # URL base de produção/dev pode mudar

# Cabeçalhos da requisição
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Corpo da requisição
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

# Enviando a requisição POST
response = requests.post(url, headers=headers, data=data)

# Verificando o status e imprimindo o token
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info.get("access_token")
    print("Token gerado com sucesso:")
    print(access_token)
else:
    print("Erro ao gerar token:")
    print(response.status_code, response.text)