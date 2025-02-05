#!/usr/bin/env python
"""
CLI entry point for the AI Enabled Test Generator.
"""

import argparse
import os
import sys
import logging
import yaml
from dotenv import load_dotenv
import shutil

from ai_engine.orchestrator import Orchestrator
from ai_engine.adapters.openai_adapter import OpenAIAdapter
from utils.config_loader import load_config

# Load environment variables before anything else
load_dotenv()

def parse_arguments():
    parser = argparse.ArgumentParser(description="AI Enabled Test Generator CLI")
    parser.add_argument(
        '--spec', required=True,
        help='Path to the API specification file (JSON/YAML)'
    )
    parser.add_argument(
        '--test-types', nargs='+', required=True,
        help='Test types to generate (functional, security, performance, e2e)'
    )
    parser.add_argument(
        '--framework', required=True,
        help='Test framework to use (e.g., pytest, jest, postman)'
    )
    parser.add_argument(
        '--output-dir', required=True,
        help='Output directory for generated tests'
    )
    return parser.parse_args()

def clean_output_directory(output_dir: str) -> None:
    """
    Clean up the output directory by removing it and recreating it.
    
    :param output_dir: Path to the output directory
    """
    if os.path.exists(output_dir):
        logging.info(f"Cleaning up existing output directory: {output_dir}")
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Created fresh output directory: {output_dir}")

def main():
    # Check for required environment variables first
    if not os.getenv("OPENAI_API_KEY"):
        logging.error("OPENAI_API_KEY environment variable is not set. Please set it in your .env file.")
        sys.exit(1)

    args = parse_arguments()

    # Clean up output directory before generating new tests
    clean_output_directory(args.output_dir)

    # Load a global configuration (if needed)
    try:
        framework_config = load_config("config/framework_config.yaml")
    except Exception as e:
        logging.error(f"Failed to load framework configuration: {e}")
        framework_config = {}

    # Load the specification file (YAML or JSON)
    try:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load specification file: {e}")
        sys.exit(1)

    # For this example, we assume the spec is already in a unified format.
    unified_spec = spec

    # Initialize the AI adapter (using OpenAI adapter for demonstration)
    try:
        adapter = OpenAIAdapter()
    except Exception as e:
        logging.error(f"Failed to initialize AI adapter: {e}")
        sys.exit(1)

    # Initialize and run the orchestrator with the unified spec and requested test types
    orchestrator = Orchestrator(adapter, unified_spec)
    results = orchestrator.run(args.test_types)

    # Save the tests to separate files
    for filename, test_code in results["test_files"].items():
        output_path = os.path.join(args.output_dir, filename)
        with open(output_path, "w") as f:
            # Add common imports and fixtures to each file
            f.write("""import pytest
import requests
import allure

@pytest.fixture
def base_url():
    return 'http://localhost:8080/api'

@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}\n\n""")
            
            f.write(test_code)
        
        logging.info(f"Generated {filename} in {args.output_dir}")

if __name__ == "__main__":
    main()
