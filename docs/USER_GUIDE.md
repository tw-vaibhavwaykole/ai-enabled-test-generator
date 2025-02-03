# User Guide

Welcome to the **AI-Enabled Test Generator**! This guide will help you get started with generating tests from your API specifications.

## Overview
The tool leverages AI to generate tests (functional, security, performance, and end-to-end) based on your API spec. It supports multiple test frameworks (e.g., pytest, jest, postman) and provides post-generation validation.

## Prerequisites

- **Python 3.7+**  
- Install required packages:
  ```bash
  pip install -r requirements.txt
  ```

- **Create a .env file in the project root with your API keys+**
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
