import os
from dotenv import load_dotenv

load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-prod")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER", "")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE", "sqldb-ops-mvp")
AZURE_SQL_USER = os.getenv("AZURE_SQL_USER", "")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD", "")
LOCAL_DEV_USER = os.getenv("LOCAL_DEV_USER", "dev@northwind.com")
LOCAL_DEV_DEPARTMENT = os.getenv("LOCAL_DEV_DEPARTMENT", "ops")
AZURE_STORAGE_OPS_CONN = os.getenv("AZURE_STORAGE_OPS_CONN", "")
AZURE_STORAGE_VENTAS_CONN = os.getenv("AZURE_STORAGE_VENTAS_CONN", "")
AZURE_STORAGE_OPS_CONTAINER = os.getenv("AZURE_STORAGE_OPS_CONTAINER", "documentos-ops")
AZURE_STORAGE_VENTAS_CONTAINER = os.getenv("AZURE_STORAGE_VENTAS_CONTAINER", "documentos-ventas")
