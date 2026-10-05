import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "speed-check"}), 200

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "running", "service": "speed-check", "port": int(os.environ.get("PORT", 8000))}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True, use_reloader=False)
