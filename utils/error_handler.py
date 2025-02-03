import logging

def handle_error(e: Exception, context: str = ""):
    """
    Handles errors in a uniform manner by logging them.
    
    :param e: The exception that occurred.
    :param context: Additional context information.
    """
    message = f"An error occurred. Context: {context}. Error: {str(e)}"
    logging.error(message)
    # Additional actions (e.g., alerting, cleanup) can be added here.
    print(message)
