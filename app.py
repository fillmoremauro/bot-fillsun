from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("📥 POST recibido en /webhook")
    print("➡️ Método:", request.method)

    if request.method == "GET":
        verify_token = "fillsun_bot_token"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        print("🔐 GET recibido para verificación")
        if mode == "subscribe" and token == verify_token:
            print("✅ Verificado correctamente")
            return challenge, 200
        else:
            print("❌ Token inválido")
            return "Token inválido", 403

    if request.method == "POST":
        try:
            print("📦 Headers:", dict(request.headers))
            print("🧾 Body:", request.data.decode("utf-8"))

            data = request.get_json()
            print("📂 JSON parseado:", data)

            if data and "entry" in data:
                entry = data["entry"][0]
                changes = entry["changes"][0]
                value = changes["value"]

                mensaje = value["messages"][0]["text"]["body"]
                numero = value["messages"][0]["from"]

                print(f"💬 Mensaje: {mensaje} | De: {numero}")

            else:
                print("⚠️ Estructura inesperada en JSON")

        except Exception as e:
            print("❗ Error procesando POST:", str(e))

        return "ok", 200

    return "Método no permitido", 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor corriendo en puerto {port}")
    app.run(host="0.0.0.0", port=port)
