import os

def get_secret(key: str) -> str:
    """
    Retrieves a secret from the environment variables.
    
    :param key: The environment variable name for the secret.
    :return: The secret value.
    :raises ValueError: If the secret is not found.
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Secret for key '{key}' not found in environment variables.")
    return value

# --- Example Usage ---
if __name__ == "__main__":
    try:
        secret = get_secret("OPENAI_API_KEY")
        print("Retrieved secret:", secret)
    except Exception as e:
        print(e)
