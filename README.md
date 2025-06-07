
# FX Matcher

A Python tool to match FX transfers between multi-currency accounts in Xero.

## IMPORTANT

To run this project, follow the steps below but first and foremost, make an .env file, a sample is shared below.

## Features

- **MOCK Mode**: Uses CSV files.
- **REAL Mode**: Uses Xero API.
- Switch modes with `MOCK=True` or `MOCK=False` in `.env`.

## Running Locally

```bash
pip install -r requirements.txt
python main.py
```

## Running with Docker

```bash
docker compose up --build
```

## Environment Variables

```
MOCK=True
XERO_CLIENT_ID=your_client_id
XERO_CLIENT_SECRET=your_client_secret
XERO_REFRESH_TOKEN=your_refresh_token
XERO_TENANT_ID=your_tenant_id
XERO_TOKEN_URL=https://identity.xero.com/connect/token
XERO_API_BASE=https://api.xero.com/api.xro/2.0
CSV_DIR=./data
FROM_ACCOUNT_ID=real-USD-account-id
TO_ACCOUNT_ID=real-AUD-account-id
```

## Outputs

- **MOCK mode**: `matched_transfers.csv`
- **REAL mode**: Posts to Xero as draft transfers

---

Enjoy! 🚀
