from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# CONFIGURACIÓN DE FILLSUN
WHATSAPP_TOKEN = "EAAJghw0LOqsBO6NSkDUKE3fR0UtXGL5NXVsm0PqJyBqOoLjSebOPihihrZAY8ZA9mV7ZB3kRSlhQ5pQHsk1SzkLzb59WlAnkqz4DRjNFuQmNBO72KqFO9Y7Uda79wmPFIsigMoWDZBrhSjATpCWGgjhMzQWCNhTArwrlZAlHHH59RgSvzIyXtUhAXlieB4gHhMFlkJaxlZAkKulSo9nUIg2xANuOlxmZBqfdhFJwnqq"
PHONE_NUMBER_ID = "598198433374729"

# URL de envío de mensajes
URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

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

    print("[ENVIANDO MENSAJE] A:", numero)
    print("Mensaje:", mensaje)

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
        print("[POST RECIBIDO EN /webhook]")
        try:
            data = request.get_json(force=True)
            print("[DATA JSON RECIBIDA]:", data)

            entry = data.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            mensajes = value.get("messages")

            if mensajes:
                mensaje = mensajes[0]["text"]["body"]
                numero = mensajes[0]["from"]
                print("Mensaje:", mensaje, "de", numero)

                if mensaje == "1":
                    respuesta = "🔆 Ahorro con termotanques solares"
                elif mensaje == "2":
                    respuesta = "⚡ Beneficios de paneles solares"
                elif mensaje == "3":
                    respuesta = "📞 Un asesor se contactará"
                else:
                    respuesta = "Seleccioná 1️⃣ 2️⃣ o 3️⃣ para comenzar."

                enviar_mensaje(numero, respuesta)
            else:
                print("[INFO] No se encontró 'messages' en el JSON")

        except Exception as e:
            print("[ERROR GRAVE] No se pudo procesar el JSON:", str(e))

        return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
