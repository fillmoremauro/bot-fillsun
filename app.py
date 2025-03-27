from flask import Flask, request
import os
import requests
import json

app = Flask(__name__)

# CONFIGURACIÓN
VERIFY_TOKEN = "fillsun_bot_token"
WHATSAPP_TOKEN = "EAAJghw0LOqsBO7rTUVZC8BlWUFjUIv2MfOXq0AxR705PwX3ZCPImHM0Ob0ZCuPQHbP9tHWykZA0xprgTAZAQXJxkXHqTdsLs3JYM6Ee3eFtBjqSPhZAbabHk9mzjZCl8ZA6kKqUXH8y3ZAafKS6HD8ZAp7w3o27hpBIVgYf7L9huWKrIC0oRycTsg8ViJ86JzSmVNnvnsYQLVENW3O3wCPzZBaj6ZAcRVPGJCdQjZCkffsOZBb"
PHONE_NUMBER_ID = "598198433374729"
API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

# ENVÍO DE MENSAJE
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
    print("📤 Enviando mensaje a:", numero)
    print("📨 Contenido:", mensaje)
    response = requests.post(API_URL, headers=headers, json=data)
    print("📬 Respuesta API:", response.status_code, response.text)

# WEBHOOK
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        print("🔍 Validación webhook: mode =", mode, " token =", token)
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Verificación exitosa")
            return challenge, 200
        else:
            print("❌ Token inválido")
            return "Token inválido", 403

    if request.method == "POST":
        print("📥 POST recibido en /webhook")
        data = request.get_json()
        print("📦 Data JSON:", json.dumps(data, indent=2))

        try:
            mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            numero = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            print("💬 Mensaje:", mensaje, "| De:", numero)

            if mensaje == "1":
                respuesta = (
                    "🔆 ¡Gran elección! Los termotanques solares pueden ayudarte a ahorrar hasta un 80% en gas o electricidad cada mes.\n"
                    "🌞 Funcionan con energía solar, te garantizan agua caliente todo el año, incluso en días nublados.\n"
                    "🔧 Mínimo mantenimiento, larga vida útil y una inversión que se paga sola en poco tiempo.\n"
                    "📲 ¿Querés ver modelos o precios?"
                )
            elif mensaje == "2":
                respuesta = (
                    "⚡ ¡Estás un paso más cerca de liberarte de las facturas de luz!\n"
                    "Los paneles solares fotovoltaicos generan tu propia electricidad y pueden reducir tu consumo hasta un 100%.\n"
                    "🌎 Energía limpia, ahorro real y aumento del valor de tu propiedad.\n"
                    "📈 Instalación profesional y asesoramiento personalizado.\n"
                    "📲 ¿Querés ver modelos o precios de kits?"
                )
            elif mensaje == "3":
                respuesta = (
                    "📞 ¡Perfecto! Un asesor de FILLSUN Argentina se va a comunicar con vos en breve.\n"
                    "💬 Podés contarnos si querés agua caliente, energía eléctrica, o ambos.\n"
                    "🚀 Cuanto más sepamos, mejor podemos ayudarte a maximizar tu ahorro.\n"
                    "¡Gracias por confiar en nosotros! 🌞"
                )
            else:
                respuesta = "Por favor, respondé con una opción válida: 1️⃣ Termotanques, 2️⃣ Paneles, 3️⃣ Asesoramiento."

            enviar_mensaje(numero, respuesta)

        except Exception as e:
            print("⚠️ Error procesando el mensaje:", str(e))

        return "ok", 200

# INICIO
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor corriendo en puerto {port}")
    app.run(host="0.0.0.0", port=port)
