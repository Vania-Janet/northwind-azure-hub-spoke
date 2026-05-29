from flask import Blueprint, render_template, request, jsonify, session
from auth import get_current_user
from ai.agent import get_ai_response

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/")
def index():
    user = get_current_user()
    return render_template("index.html", user=user)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    user = get_current_user()
    data = request.get_json(silent=True)

    if not data or not data.get("message"):
        return jsonify({"error": "Mensaje vacío"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Mensaje vacío"}), 400

    department = user["department"]

    if "history" not in session:
        session["history"] = []

    history = session["history"]

    try:
        reply = get_ai_response(user_message, department, history)
    except Exception as e:
        return jsonify({"error": f"Error del agente IA: {str(e)}"}), 500

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    session["history"] = history[-20:]

    return jsonify({"reply": reply})


@chat_bp.route("/api/chat/clear", methods=["POST"])
def clear_history():
    session.pop("history", None)
    return jsonify({"ok": True})
