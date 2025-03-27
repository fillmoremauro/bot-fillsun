from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("📥 Entró al webhook")
    print("➡️ Método:", request.method)

    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == "fillsun_bot_token":
            print("✅ Verificación exitosa")
            return challenge, 200
        return "Token inválido", 403

    if request.method == "POST":
        print("✅ POST recibido")
        try:
            data = request.get_json()
            print("🧾 DATA:", data)
        except Exception as e:
            print("❌ Error parseando JSON:", e)
        return "ok", 200

    return "Método no permitido", 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
