from flask import Flask, request
import os
import json

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    print("📬 WEBHOOK ACTIVADO", flush=True)
    print("🔁 Método:", request.method, flush=True)

    if request.method == "GET":
        verify_token = "fillsun_bot_token"
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        print("🔍 Verificando token...", flush=True)
        if mode == "subscribe" and token == verify_token:
            print("✅ VERIFICADO", flush=True)
            return challenge, 200
        else:
            print("❌ Token inválido", flush=True)
            return "Token inválido", 403

    if request.method == "POST":
        print("📥 POST RECIBIDO EN /webhook", flush=True)
        headers = dict(request.headers)
        print("🔍 Headers:", headers, flush=True)

        try:
            raw_data = request.data.decode("utf-8")
            print("🧾 Raw body:", raw_data, flush=True)

            data = json.loads(raw_data)
            print("📦 JSON parseado:", json.dumps(data, indent=2), flush=True)

            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])

            if messages:
                msg = messages[0]
                numero = msg.get("from")
                texto = msg.get("text", {}).get("body")
                print(f"✅ Mensaje recibido de {numero}: {texto}", flush=True)
            else:
                print("⚠️ No hay mensajes en el webhook", flush=True)

        except Exception as e:
            print("🛑 ERROR en procesamiento:", e, flush=True)

        return "ok", 200

    return "Método no permitido", 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Iniciando servidor en puerto {port}...", flush=True)
    app.run(host="0.0.0.0", port=port)
