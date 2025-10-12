import mercadopago
import base64

sdk = mercadopago.SDK("APP_USR-5145246492937894-082615-7c297dd6304b1d2eff3324ca7634427f-385326403")

payment_data = {
    "transaction_amount": 25.50,
    "description": "Aposta no Clube da Sinuca 🎯",
    "payment_method_id": "pix",
    "payer": {
        "email": "cliente@teste.com"
    }
}

payment_response = sdk.payment().create(payment_data)
payment = payment_response["response"]

# Exibir QR Code em base64
qr_base64 = payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
qr_code_img = base64.b64decode(qr_base64)

with open("qrcode_pix.png", "wb") as f:
    f.write(qr_code_img)

print("QR Code gerado: qrcode_pix.png")
print("Copia e cola PIX:", payment["point_of_interaction"]["transaction_data"]["qr_code"])
