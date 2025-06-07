import logging

# Setting up basic logging here only. Not sure about exact requirements.

def get_logger(name: str = "fx_matcher"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Avoid adding duplicate handlers
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
