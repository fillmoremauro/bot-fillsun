from flask import Flask, request
import requests

app = Flask(__name__)

# CONFIGURACIÓN DE FILLSUN
WHATSAPP_TOKEN = "EAAJghw0LOqsBOZCw4SZB0gVjskjsJHBcBRbZAIgPikqWZABjzy9WhlHvnaU9dlZAwZCdkQpoEdFoaZCgYxtFvZBAkeN6XRwkRAeJ6vqOgD5u8GsSDNzKu9RZBq4VxCIYxNBGbZCnKWKXzyiqRH152yuI0OBwFO7yVt3uiQZAdQEMyIBkaCQuUu0QcRt11fdQZBNKuhpQCBNEjqa4cYKoLOvC2cnknkUmgXMoU8q12OZBj77oA"
PHONE_NUMBER_ID = "541133480020"

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
    requests.post(URL, headers=headers, json=data)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificación del webhook
        verify_token = "fillsun_bot_token"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Unauthorized", 403

    if request.method == "POST":
        data = request.get_json()

        try:
            mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            numero = data['entry'][0]['changes'][0]['value']['messages'][0]['from']

            if mensaje == "1":
                respuesta = "🔆 Los termotanques solares permiten ahorrar hasta un 80% en gas o electricidad. Agua caliente todo el año! 🚿"
            elif mensaje == "2":
                respuesta = "⚡ Los paneles solares generan electricidad y reducen tu factura de luz. Energía limpia y retorno rápido. ☀️"
            elif mensaje == "3":
                respuesta = "📞 Un asesor de FILLSUN se comunicará con vos a la brevedad. Gracias por tu interés. 💬"
            else:
                respuesta = "Por favor, respondé con una opción válida: 1️⃣ Termotanques, 2️⃣ Paneles, 3️⃣ Asesoramiento."

            enviar_mensaje(numero, respuesta)

        except Exception as e:
            print("[ERROR]", e)

        return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
