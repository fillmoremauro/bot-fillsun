from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    verify_token = "fillsun_bot_token"
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return challenge, 200
    else:
        return "Token inválido", 403

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


