from flask import Blueprint, request, jsonify

bp = Blueprint("chat", __name__, url_prefix="/chat")

@bp.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    return jsonify({"reply": "Demo response from backend"})