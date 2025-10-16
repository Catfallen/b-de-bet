import requests

def getSaldo(token):
    try:
        url = "http://localhost:3000/payments/saldo"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.post(url, headers=headers)

        if r.status_code == 200:
            data = r.json()
            saldo_str = data.get("saldo", "0")
            print(saldo_str)
            try:
                saldo = float(saldo_str)
            except ValueError:
                saldo = 0.0
        else:
            print(f"Erro ao consultar saldo: {r.status_code} - {r.text}")
            saldo = 0.0
    except Exception as e:
        print(f"Erro na requisição de saldo: {e}")
        saldo = 0.0

    return saldo