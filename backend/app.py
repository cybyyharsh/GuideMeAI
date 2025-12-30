from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------- HEALTH CHECK ----------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# ---------- ROOT (OPTIONAL BUT USEFUL) ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "GuideMeAI backend running"}), 200