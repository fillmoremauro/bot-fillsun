from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# Token actualizado que me pasaste
WHATSAPP_TOKEN = "EAAJghw0LOqsBO7rTUVZC8BlWUFjUIv2MfOXq0AxR705PwX3ZCPImHM0Ob0ZCuPQHbP9tHWykZA0xprgTAZAQXJxkXHqTdsLs3JYM6Ee3eFtBjqSPhZAbabHk9mzjZCl8ZA6kKqUXH8y3ZAafKS6HD8ZAp7w3o27hpBIVgYf7L9huWKrIC0oRycTsg8ViJ86JzSmVNnvnsYQLVENW3O3wCPzZBaj6ZAcRVPGJCdQjZCkffsOZBb"
PHONE_NUMBER_ID = "598198433374729"
URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("📬 WEBHOOK ACTIVADO", flush=True)
    print("🔁 Método:", request.method, flush=True)

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
        print("📥 POST RECIBIDO EN /webhook", flush=True)
        try:
            data = request.get_json()
            print("🧾 Raw body:", json.dumps(data, indent=2), flush=True)

            value = data['entry'][0]['changes'][0]['value']
            message = value.get('messages', [{}])[0]
            numero = message.get('from')
            texto = message.get('text', {}).get('body', '')

            print(f"✅ Mensaje recibido de {numero}: {texto}", flush=True)

            # Generar respuesta
            if texto == "1":
                respuesta = (
                    "🔆 ¡Gran elección! Los termotanques solares pueden ayudarte a ahorrar hasta un 80% en gas o electricidad cada mes.\n"
                    "🌞 Funcionan con energía solar, te garantizan agua caliente todo el año, incluso en días nublados.\n"
                    "🔧 Mínimo mantenimiento, larga vida útil y una inversión que se paga sola en poco tiempo.\n"
                    "📲 ¿Querés ver modelos o precios?"
                )
            elif texto == "2":
                respuesta = (
                    "⚡ ¡Estás un paso más cerca de liberarte de las facturas de luz!\n"
                    "Los paneles solares fotovoltaicos generan tu propia electricidad y pueden reducir tu consumo hasta un 100%.\n"
                    "🌎 Energía limpia, ahorro real y aumento del valor de tu propiedad.\n"
                    "📈 Instalación profesional y asesoramiento personalizado.\n"
                    "📲 ¿Querés ver modelos o precios de kits?"
                )
            elif texto == "3":
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
            print("❌ ERROR AL PROCESAR POST:", e, flush=True)

        return "ok", 200

def enviar_mensaje(numero, mensaje):
    print(f"📤 Enviando mensaje a {numero}", flush=True)
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

    try:
        response = requests.post(URL, headers=headers, json=data)
        print(f"📨 Estado: {response.status_code}", flush=True)
        print(f"📨 Respuesta API: {response.text}", flush=True)
    except Exception as e:
        print("❌ ERROR AL ENVIAR MENSAJE:", e, flush=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
