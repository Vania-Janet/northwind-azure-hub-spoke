from flask import Blueprint, jsonify
import config

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health():
    return jsonify({"status": "ok"})


@health_bp.route("/health/sql")
def health_sql():
    if not config.AZURE_SQL_SERVER:
        return jsonify({"status": "skip", "reason": "AZURE_SQL_SERVER not set"}), 200
    try:
        import pymssql
        conn = pymssql.connect(
            server=config.AZURE_SQL_SERVER,
            user=config.AZURE_SQL_USER,
            password=config.AZURE_SQL_PASSWORD,
            database=config.AZURE_SQL_DATABASE,
            timeout=5,
        )
        conn.close()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500
