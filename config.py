import os
from dotenv import load_dotenv

load_dotenv()

MOCK_MODE = os.getenv("MOCK", "True").lower() == "true"
XERO_CLIENT_ID = os.getenv("XERO_CLIENT_ID")
XERO_CLIENT_SECRET = os.getenv("XERO_CLIENT_SECRET")
XERO_REFRESH_TOKEN = os.getenv("XERO_REFRESH_TOKEN")
XERO_TENANT_ID = os.getenv("XERO_TENANT_ID")
CSV_DIR = os.getenv("CSV_DIR", "./data")
XERO_TOKEN_URL = os.getenv("XERO_TOKEN_URL", "https://identity.xero.com/connect/token")
XERO_API_BASE = os.getenv("XERO_API_BASE", "https://api.xero.com/api.xro/2.0")
FROM_ACCOUNT_ID = os.getenv("FROM_ACCOUNT_ID")
TO_ACCOUNT_ID = os.getenv("TO_ACCOUNT_ID")

