from flask import Blueprint, jsonify, Response
from auth import get_current_user
import config

files_bp = Blueprint("files", __name__)

_DEPT_CONTAINERS = {
    "ops": lambda: config.AZURE_STORAGE_OPS_CONTAINER,
    "ventas": lambda: config.AZURE_STORAGE_VENTAS_CONTAINER,
}

_TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".xml", ".log", ".py", ".html"}


def _fmt_size(size_bytes):
    if size_bytes is None or size_bytes == 0:
        return "0 B"
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def _get_container_client(dept):
    container_fn = _DEPT_CONTAINERS.get(dept)
    if not container_fn or not config.AZURE_STORAGE_CONN:
        return None, None
    from azure.storage.blob import BlobServiceClient
    client = BlobServiceClient.from_connection_string(config.AZURE_STORAGE_CONN)
    return client, client.get_container_client(container_fn())


@files_bp.route("/api/files")
def list_files():
    user = get_current_user()
    dept = user["department"]

    if not config.AZURE_STORAGE_CONN:
        return jsonify({"files": [], "error": "Almacenamiento no configurado aún"}), 200

    try:
        _, container_client = _get_container_client(dept)
        if container_client is None:
            return jsonify({"files": [], "error": "Departamento sin almacenamiento configurado"}), 200

        blobs = [
            {"name": b.name, "size": _fmt_size(b.size)}
            for b in container_client.list_blobs()
        ]
        return jsonify({"files": blobs, "department": dept, "container": container_client.container_name})
    except Exception as e:
        return jsonify({"files": [], "error": str(e)}), 500


@files_bp.route("/api/files/<path:filename>")
def get_file(filename):
    user = get_current_user()
    dept = user["department"]

    if not config.AZURE_STORAGE_CONN:
        return jsonify({"error": "Almacenamiento no configurado"}), 503

    try:
        client, container_client = _get_container_client(dept)
        if container_client is None:
            return jsonify({"error": "Departamento sin almacenamiento configurado"}), 404

        blob_client = client.get_blob_client(
            container=container_client.container_name, blob=filename
        )
        ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

        if ext in _TEXT_EXTENSIONS:
            content = blob_client.download_blob().readall().decode("utf-8", errors="replace")
            return jsonify({"content": content, "type": "text"})

        return jsonify({"content": None, "type": "binary", "message": "Vista previa no disponible para este tipo de archivo."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
