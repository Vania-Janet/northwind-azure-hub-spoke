from flask import Blueprint, jsonify
from auth import get_current_user
import config

files_bp = Blueprint("files", __name__)

_STORAGE_CONFIG = {
    "ops": {
        "conn": lambda: config.AZURE_STORAGE_OPS_CONN,
        "container": lambda: config.AZURE_STORAGE_OPS_CONTAINER,
    },
    "ventas": {
        "conn": lambda: config.AZURE_STORAGE_VENTAS_CONN,
        "container": lambda: config.AZURE_STORAGE_VENTAS_CONTAINER,
    },
}


@files_bp.route("/api/files")
def list_files():
    user = get_current_user()
    dept = user["department"]

    cfg = _STORAGE_CONFIG.get(dept)
    if not cfg:
        return jsonify({"files": [], "error": "Departamento sin almacenamiento configurado"}), 200

    conn_str = cfg["conn"]()
    container = cfg["container"]()

    if not conn_str:
        return jsonify({"files": [], "error": "Almacenamiento no configurado aún"}), 200

    try:
        from azure.storage.blob import BlobServiceClient
        client = BlobServiceClient.from_connection_string(conn_str)
        container_client = client.get_container_client(container)
        blobs = [
            {"name": b.name, "size_kb": round((b.size or 0) / 1024, 1)}
            for b in container_client.list_blobs()
        ]
        return jsonify({"files": blobs, "department": dept, "container": container})
    except Exception as e:
        return jsonify({"files": [], "error": str(e)}), 500
