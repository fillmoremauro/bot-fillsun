from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("📥 Entró al webhook")
    print("➡️ Método recibido:", request.method)

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
        print("✅ LLEGÓ UN POST A /webhook")
        print("🔍 Headers:", dict(request.headers))
        print("🧾 Body (raw):", request.data.decode("utf-8"))
        return "ok", 200

    return "Método no permitido", 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
