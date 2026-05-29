import os

_DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")

_DEPT_FOLDER = {
    "ops": "ops",
    "ventas": "ventas",
}


def load_context(department: str) -> str:
    folder = _DEPT_FOLDER.get(department, "ops")
    docs_path = os.path.join(_DOCS_DIR, folder)

    if not os.path.isdir(docs_path):
        return ""

    texts = []
    for filename in sorted(os.listdir(docs_path)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(docs_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                texts.append(f"=== {filename} ===\n{content}")
        except OSError:
            continue

    return "\n\n".join(texts)
