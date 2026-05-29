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
    result = {}
    try:
        import pymssql
        conn = pymssql.connect(
            server=config.AZURE_SQL_SERVER,
            user=config.AZURE_SQL_USER,
            password=config.AZURE_SQL_PASSWORD,
            database=config.AZURE_SQL_DATABASE,
            timeout=5,
        )
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM sys.tables WHERE name = 'chat_history'")
        result["table_exists"] = cur.fetchone()[0] == 1

        cur.execute("INSERT INTO chat_history (user_id, department, role, content) VALUES (%s, %s, %s, %s)",
                    ("__healthcheck__", "test", "user", "ping"))
        conn.commit()
        result["insert"] = "ok"

        cur.execute("SELECT COUNT(*) FROM chat_history WHERE user_id = %s", ("__healthcheck__",))
        result["rows_after_insert"] = cur.fetchone()[0]

        cur.execute("SELECT TOP 5 user_id, role, content FROM chat_history WHERE user_id != '__healthcheck__' ORDER BY id DESC")
        result["last_real_rows"] = [{"user_id": r[0], "role": r[1], "content": r[2][:50]} for r in cur.fetchall()]

        cur.execute("DELETE FROM chat_history WHERE user_id = %s", ("__healthcheck__",))
        conn.commit()
        conn.close()
        result["status"] = "ok"
        return jsonify(result)
    except Exception as e:
        result["status"] = "error"
        result["detail"] = str(e)
        return jsonify(result), 500
