import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def welcome():
    return "OK", 200

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, threaded=True)
