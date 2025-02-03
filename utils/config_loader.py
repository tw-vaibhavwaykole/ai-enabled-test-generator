import yaml

def load_config(config_path: str) -> dict:
    """
    Loads a YAML configuration file and returns its content as a dictionary.
    
    :param config_path: Path to the YAML configuration file.
    :return: A dictionary containing configuration data.
    :raises RuntimeError: If the configuration file cannot be loaded.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load config file '{config_path}': {e}") from e

# --- Example Usage ---
if __name__ == "__main__":
    config = load_config("ai-test-generator/config/ai_providers.yaml")
    print(config)
