from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

WHATSAPP_TOKEN = "EAAJghw0LOqsBO6NSkDUKE3fR0UtXGL5NXVsm0PqJyBqOoLjSebOPihihrZAY8ZA9mV7ZB3kRSlhQ5pQHsk1SzkLzb59WlAnkqz4DRjNFuQmNBO72KqFO9Y7Uda79wmPFIsigMoWDZBrhSjATpCWGgjhMzQWCNhTArwrlZAlHHH59RgSvzIyXtUhAXlieB4gHhMFlkJaxlZAkKulSo9nUIg2xANuOlxmZBqfdhFJwnqq"
PHONE_NUMBER_ID = "598198433374729"
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
    print("🔁 Enviando mensaje a", numero)
    print("📨 Contenido:", mensaje)
    response = requests.post(URL, headers=headers, json=data)
    print("✅ Status:", response.status_code)
    print("📩 Respuesta API:", response.text)

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
        print("🔔 [POST RECIBIDO EN /webhook] 🔔")

        try:
            raw_body = request.data.decode("utf-8")
            print("🧾 Cuerpo crudo:", raw_body)

            data = request.get_json(force=True)
            print("📦 JSON parseado:", json.dumps(data, indent=2))

            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            print("🔑 Campos recibidos:", list(value.keys()))

            if "messages" in value:
                mensaje = value["messages"][0]["text"]["body"]
                numero = value["messages"][0]["from"]
                print("📥 Mensaje recibido:", mensaje, "de", numero)

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
                        "Por favor, respondé con una opción válida:\n"
                        "1️⃣ Termotanques\n2️⃣ Paneles\n3️⃣ Asesoramiento"
                    )

                enviar_mensaje(numero, respuesta)
            else:
                print("⚠️ No se encontró 'messages' en el webhook recibido.")

        except Exception as e:
            print("❌ [ERROR AL PROCESAR POST]:", e)

        return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
