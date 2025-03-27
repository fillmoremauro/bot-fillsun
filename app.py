from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

ACCESS_TOKEN = "EAAJghw0LOqsBO7rTUVZC8BlWUFjUIv2MfOXq0AxR705PwX3ZCPImHM0Ob0ZCuPQHbP9tHWykZA0xprgTAZAQXJxkXHqTdsLs3JYM6Ee3eFtBjqSPhZAbabHk9mzjZCl8ZA6kKqUXH8y3ZAafKS6HD8ZAp7w3o27hpBIVgYf7L9huWKrIC0oRycTsg8ViJ86JzSmVNnvnsYQLVENW3O3wCPzZBaj6ZAcRVPGJCdQjZCkffsOZBb"
PHONE_ID = "598198433374729"

@app.route("/")
def index():
    return "Bot FILLSUN operativo", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        VERIFY_TOKEN = "fillsun_bot_token"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Token inválido", 403

    if request.method == "POST":
        print("✅ POST recibido en /webhook")
        data = request.get_json()
        print("🧾 JSON recibido:", json.dumps(data, indent=2))

        try:
            mensajes = data["entry"][0]["changes"][0]["value"]["messages"]
            if mensajes:
                mensaje = mensajes[0]["text"]["body"]
                numero = mensajes[0]["from"]
                print(f"📨 Mensaje recibido: {mensaje} de {numero}")

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
                    respuesta = (
                        "🤖 No entiendo tu mensaje.\n"
                        "Por favor respondé con una opción válida:\n"
                        "1️⃣ Termotanques\n2️⃣ Paneles\n3️⃣ Asesoramiento"
                    )

                enviar_mensaje(numero, respuesta)
        except Exception as e:
            print("⚠️ Error procesando el webhook:", e)

        return "ok", 200

def enviar_mensaje(numero, texto):
    url = f"https://graph.facebook.com/v17.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": texto}
    }

    print("📤 Enviando respuesta...")
    res = requests.post(url, headers=headers, json=payload)
    print("📬 Status:", res.status_code)
    print("📩 Respuesta:", res.text)

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
