import os
from dotenv import load_dotenv

load_dotenv()

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-prod")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
AZURE_SQL_CONNECTION_STRING = os.getenv("AZURE_SQL_CONNECTION_STRING", "")
LOCAL_DEV_USER = os.getenv("LOCAL_DEV_USER", "dev@northwind.com")
LOCAL_DEV_DEPARTMENT = os.getenv("LOCAL_DEV_DEPARTMENT", "ops")
