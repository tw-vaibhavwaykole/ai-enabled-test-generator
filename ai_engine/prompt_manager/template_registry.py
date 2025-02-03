# ai-test-generator/ai_engine/prompt_manager/template_registry.py

import os
import re
from typing import Dict, Any


class TemplateRegistry:
    """
    Manages and registers versioned prompt templates.

    The registry scans a base directory containing subdirectories (categories)
    such as 'functional' and 'security', and loads all Jinja2 templates found.
    Templates should follow the naming convention:
        <template_name>_v<version_number>.jinja
    For example: default_v1.jinja, custom_v2.jinja
    """

    def __init__(self, base_dir: str):
        """
        Initializes the registry by loading templates from the base directory.

        :param base_dir: The base directory path for the templates.
                         e.g., "ai-test-generator/ai_engine/prompt_manager/jinja_templates"
        """
        self.base_dir = base_dir
        # Structure: { category: { template_name: { version_number: template_content } } }
        self.templates: Dict[str, Dict[str, Dict[int, str]]] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """
        Scans the base directory and loads templates into the registry.
        """
        if not os.path.isdir(self.base_dir):
            raise FileNotFoundError(f"Template base directory '{self.base_dir}' not found.")

        for category in os.listdir(self.base_dir):
            category_path = os.path.join(self.base_dir, category)
            if os.path.isdir(category_path):
                self.templates[category] = {}
                for filename in os.listdir(category_path):
                    if filename.endswith(".jinja"):
                        # Expected pattern: <template_name>_v<version>.jinja
                        match = re.match(r"^(?P<name>.+)_v(?P<version>\d+)\.jinja$", filename)
                        if match:
                            template_name = match.group("name")
                            version = int(match.group("version"))
                        else:
                            # If no version is specified, default to version 1 using filename without extension.
                            template_name = os.path.splitext(filename)[0]
                            version = 1

                        file_path = os.path.join(category_path, filename)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                        except Exception as e:
                            raise RuntimeError(f"Error reading template file '{file_path}': {e}") from e

                        if template_name not in self.templates[category]:
                            self.templates[category][template_name] = {}
                        self.templates[category][template_name][version] = content

    def get_template(self, category: str, template_name: str, version: str = "latest") -> str:
        """
        Retrieves a template by category, name, and version.

        :param category: The template category (e.g., 'functional' or 'security').
        :param template_name: The base name of the template (e.g., 'default').
        :param version: The version to retrieve (e.g., '1') or 'latest' for the highest version.
        :return: The template content as a string.
        :raises ValueError: If the specified template or version is not found.
        """
        if category not in self.templates:
            raise ValueError(f"No templates found for category '{category}'.")
        if template_name not in self.templates[category]:
            raise ValueError(f"No template named '{template_name}' found in category '{category}'.")

        versions: Dict[int, str] = self.templates[category][template_name]
        if version == "latest":
            latest_version = max(versions.keys())
            return versions[latest_version]
        else:
            try:
                version_num = int(version)
            except ValueError:
                raise ValueError("Version must be an integer or 'latest'.")
            if version_num in versions:
                return versions[version_num]
            else:
                raise ValueError(
                    f"Version {version} of template '{template_name}' not found in category '{category}'."
                )

    def list_templates(self, category: str = None) -> Dict[str, Any]:
        """
        Lists the available templates.

        :param category: If provided, lists templates for that category; otherwise, lists all.
        :return: A dictionary of available templates.
        """
        if category:
            return self.templates.get(category, {})
        return self.templates


# --- Example Usage ---
# if __name__ == "__main__":
#     # Assume the base directory for templates is:
#     base_dir = "ai-test-generator/ai_engine/prompt_manager/jinja_templates"
#     registry = TemplateRegistry(base_dir)
#
#     # List all available templates.
#     all_templates = registry.list_templates()
#     print("All Templates Loaded:")
#     print(all_templates)
#
#     # Retrieve the latest version of the 'default' functional template.
#     try:
#         functional_template = registry.get_template("functional", "default", version="latest")
#         print("\nRetrieved Functional Template (latest):")
#         print(functional_template)
#     except ValueError as e:
#         print(f"Error: {e}")
