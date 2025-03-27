from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# CONFIGURACIÓN DE FILLSUN
WHATSAPP_TOKEN = "EAAJghw0LOqsBOZCw4SZB0gVjskjsJHBcBRbZAIgPikqWZABjzy9WhlHvnaU9dlZAwZCdkQpoEdFoaZCgYxtFvZBAkeN6XRwkRAeJ6vqOgD5u8GsSDNzKu9RZBq4VxCIYxNBGbZCnKWKXzyiqRH152yuI0OBwFO7yVt3uiQZAdQEMyIBkaCQuUu0QcRt11fdQZBNKuhpQCBNEjqa4cYKoLOvC2cnknkUmgXMoU8q12OZBj77oA"
PHONE_NUMBER_ID = "598198433374729"

# URL de envío de mensajes
URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# Función para enviar mensajes por WhatsApp
def enviar_mensaje(numero, mensaje):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensaje}
    }

    print("[ENVIANDO MENSAJE]")
    print("A:", numero)
    print("Mensaje:", mensaje)
    print("Payload:", data)

    response = requests.post(URL, headers=headers, json=data)
    print("Respuesta de la API:", response.status_code, response.text)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = "fillsun_bot_token"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Token inválido", 403

    if request.method == "POST":
        data = request.get_json()

        print("[WEBHOOK RECIBIDO] RAW JSON:")
        print(json.dumps(data, indent=2))

        return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

