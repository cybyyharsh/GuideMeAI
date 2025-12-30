from flask import Flask
from flask_cors import CORS
from backend.routes.chat import bp as chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp)

@app.route("/health")
def health():
    return {"status": "ok"}