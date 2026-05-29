import base64
import json
from flask import request
import config

_DEPT_KEYWORDS = {
    "ventas": ["ventas", "sales"],
    "ops": ["ops", "operaciones", "operations", "logistics", "logistica"],
}


def get_current_user():
    header = request.headers.get("X-MS-CLIENT-PRINCIPAL")

    if header:
        try:
            decoded = base64.b64decode(header).decode("utf-8")
            principal = json.loads(decoded)
            claims = _claims_dict(principal)

            name = (
                claims.get("name")
                or claims.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name")
                or claims.get("preferred_username", "Usuario")
            )
            email = claims.get("preferred_username", "")
            department = _detect_department(claims, principal)

            return {"name": name, "email": email, "department": department}
        except Exception:
            pass

    return {
        "name": config.LOCAL_DEV_USER,
        "email": config.LOCAL_DEV_USER,
        "department": config.LOCAL_DEV_DEPARTMENT,
    }


def _claims_dict(principal):
    result = {}
    for c in principal.get("claims", []):
        result[c["typ"]] = c["val"]
    return result


def _detect_department(claims, principal):
    # 1. App Roles (configured in Entra ID App Registration — most reliable)
    roles_raw = claims.get("roles", "")
    for dept, keywords in _DEPT_KEYWORDS.items():
        if any(k in roles_raw.lower() for k in keywords):
            return dept

    # 2. Multi-value roles claim (comes as repeated entries in the claims array)
    for c in principal.get("claims", []):
        if c["typ"] == "roles":
            val = c["val"].lower()
            for dept, keywords in _DEPT_KEYWORDS.items():
                if any(k in val for k in keywords):
                    return dept

    # 3. Keyword scan across all claim values (groups, jobTitle, department, email)
    all_values = " ".join(str(v) for v in claims.values()).lower()
    for dept, keywords in _DEPT_KEYWORDS.items():
        if any(k in all_values for k in keywords):
            return dept

    return "ops"
