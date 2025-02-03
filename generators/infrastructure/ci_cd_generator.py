# ai-test-generator/generators/infrastructure/ci_cd_generator.py

import os
import yaml

class CiCdGenerator:
    """
    Generates CI/CD pipeline configuration files based on provided parameters.
    Currently supports generation of a GitHub Actions workflow YAML file.
    """

    def __init__(self, config: dict = None):
        """
        :param config: Optional dictionary containing CI/CD configuration settings.
        """
        self.config = config or self.default_config()

    def default_config(self) -> dict:
        """
        Returns the default CI/CD configuration.
        """
        return {
            "name": "CI Pipeline",
            "on": ["push", "pull_request"],
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"name": "Checkout code", "uses": "actions/checkout@v2"},
                        {
                            "name": "Set up Python",
                            "uses": "actions/setup-python@v2",
                            "with": {"python-version": "3.8"}
                        },
                        {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
                        {"name": "Run tests", "run": "pytest"}
                    ]
                }
            }
        }

    def generate_pipeline(self, output_path: str) -> None:
        """
        Generates the CI/CD pipeline configuration file.
        
        :param output_path: Path where the pipeline configuration file should be saved.
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, sort_keys=False)
            print(f"CI/CD pipeline configuration generated at: {output_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate CI/CD pipeline configuration: {e}") from e


# --- Example Usage ---
# if __name__ == "__main__":
#     generator = CiCdGenerator()
#     generator.generate_pipeline("ci_cd_pipeline.yml")
