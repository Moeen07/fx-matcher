from config import MOCK_MODE
from services import matcher
from utils.logger import get_logger

logger = get_logger()

def main():
    if MOCK_MODE:
        logger.info("🔧 Running in MOCK mode with CSV data.")
        transactions = matcher.load_csv_transactions()
    else:
        logger.info("🔗 Running in REAL mode with Xero API.")
        transactions = matcher.load_xero_transactions()

    logger.info(f"✅ Loaded {len(transactions)} transactions.")

    matches = matcher.match_transfers(transactions)
    logger.info(f"🔎 Found {len(matches)} matching transfers.")

    if MOCK_MODE:
        matcher.save_matches_to_csv(matches)
        logger.info("📁 Matches saved to matched_transfers.csv.")
    else:
        matcher.post_matches_to_xero(matches)
        logger.info("🚀 Draft transfers posted to Xero.")

if __name__ == "__main__":
    main()
