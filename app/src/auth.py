import base64
import json
from flask import request
import config


def get_current_user():
    header = request.headers.get("X-MS-CLIENT-PRINCIPAL")

    if header:
        try:
            decoded = base64.b64decode(header).decode("utf-8")
            principal = json.loads(decoded)
            claims = {c["typ"]: c["val"] for c in principal.get("claims", [])}

            name = claims.get("name", claims.get("preferred_username", "Usuario"))
            email = claims.get("preferred_username", "")
            department = _detect_department(claims)

            return {"name": name, "email": email, "department": department}
        except Exception:
            pass

    return {
        "name": config.LOCAL_DEV_USER,
        "email": config.LOCAL_DEV_USER,
        "department": config.LOCAL_DEV_DEPARTMENT,
    }


def _detect_department(claims):
    all_values = " ".join(str(v) for v in claims.values()).lower()
    if "ventas" in all_values or "sales" in all_values:
        return "ventas"
    return "ops"
