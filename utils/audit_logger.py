import logging
from datetime import datetime

LOG_FILE = "audit.log"

def setup_audit_logger(log_file: str = None):
    """
    Sets up and returns an audit logger.
    """
    if log_file is None:
        log_file = LOG_FILE
    logger = logging.getLogger("audit")
    logger.setLevel(logging.INFO)
    # Avoid adding multiple handlers if logger is already configured.
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger

def log_event(event: str, level: str = "info"):
    """
    Logs an audit event.
    """
    logger = setup_audit_logger()
    level = level.lower()
    if level == "info":
        logger.info(event)
    elif level == "warning":
        logger.warning(event)
    elif level == "error":
        logger.error(event)
    else:
        logger.info(event)

# --- Example Usage ---
if __name__ == "__main__":
    log_event("Test generation started.")
    log_event("Test generation completed successfully.", level="info")
