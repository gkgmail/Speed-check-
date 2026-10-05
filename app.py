import os
from flask import Flask
import asyncio

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

@app.route("/status", methods=["GET"])
def status():
    return {"status": "running", "version": "3.1.0"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Use production-ready settings
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        threaded=True,
        use_reloader=False,
    )
