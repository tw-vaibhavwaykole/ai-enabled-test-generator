# Developer Guide

Welcome to the **AI-Enabled Test Generator** project! This guide is intended for developers looking to understand, extend, or contribute to the project.

## Overview
This project generates test cases using AI based on provided API specifications. The architecture is modular, following clean code principles to allow for easy extension and maintenance.

## Project Structure

- **core/**  
  Contains domain logic and specification processing.
  - **spec_processor/**: Handles loading, validating, analyzing, and normalizing API specifications.
  - **test_models/**: Defines the data models for test cases and test suites.

- **ai_engine/**  
  Contains the AI integration and test generation logic.
  - **adapters/**: Provides a unified interface and concrete implementations for different AI providers.
  - **generators/**: Contains test-type–specific generators (functional, security, performance, e2e).
  - **post_processor/**: Contains post-generation validation (syntax checking, spec compliance, security scanning).
  - **prompt_manager/**: Manages prompt templates (using Jinja2) for dynamic prompt composition.

- **generators/**  
  Contains framework-specific implementations and environment generators.
  - **framework_adapters/**: Contains adapters for various test frameworks (pytest, jest, postman).
  - **infrastructure/**: Contains modules to generate Dockerfiles and CI/CD pipeline configurations.
  - **test_assembler.py**: Combines AI output with static templates to produce final test files.

- **config/**  
  Centralized configuration files for AI providers, framework settings, generation rules, and model mappings.

- **interfaces/**  
  Contains system entry points (e.g., the CLI).

- **utils/**  
  Contains shared utility functions and modules.

- **templates/**  
  Contains static template assets for tests and infrastructure.

- **artifacts/**  
  Contains generation outputs (tests and reports).

- **docs/**  
  Contains project documentation (this file and the User Guide).

## Development Guidelines

- **Coding Standards:**  
  Follow PEP8 guidelines for Python code. Ensure your code is modular, well-documented, and covered by tests.

- **Modularity:**  
  Each module should be responsible for a single aspect of the system. Avoid monolithic code.

- **Documentation:**  
  Update this guide and inline comments as you add new features or modules.

- **Testing:**  
  Write unit tests for new functionality and ensure all tests pass before committing changes.

- **Version Control:**  
  Use Git for version control. Follow commit message guidelines and create pull requests for code reviews.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Write your code, tests, and update the documentation as needed.
4. Submit a pull request for review.

Happy coding and thank you for contributing!
