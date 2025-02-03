#!/usr/bin/env python
"""
CLI entry point for the AI Enabled Test Generator.
"""

import argparse
import os
import sys
import logging
import yaml

from ai_engine.orchestrator import Orchestrator
from ai_engine.adapters.openai_adapter import OpenAIAdapter
from utils.config_loader import load_config

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

def main():
    args = parse_arguments()

    # Load a global configuration (if needed)
    try:
        framework_config = load_config("ai-test-generator/config/framework_config.yaml")
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

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, "generated_tests.txt")

    # Write the aggregated test suites to the output file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Generated Test Suites:\n")
            for test_type, suite in results.items():
                f.write(f"\n--- {test_type.upper()} TESTS ---\n")
                f.write(str(suite))
                f.write("\n")
        print(f"Generated tests saved to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write output: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
