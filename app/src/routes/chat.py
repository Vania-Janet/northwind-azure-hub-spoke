from flask import Blueprint, render_template
from auth import get_current_user

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/")
def index():
    user = get_current_user()
    return render_template("index.html", user=user)
