AI-Enabled Test Generator
=========================

This project leverages AI to generate tests (functional, security, performance, and end-to-end) from API
specifications. It supports multiple test frameworks (such as pytest, jest, and postman) and includes
post-generation validations like syntax checking, specification compliance, and security scanning.

Features
--------
- Spec Processing: Load, validate, analyze, and normalize API specifications.
- AI Integration: Generate tests using providers such as OpenAI, Gemini, and Hugging Face.
- Test Generation: Supports functional, security, performance, and end-to-end test generation.
- Framework Adapters: Integrations for frameworks like pytest, jest, and postman.
- Infrastructure Generators: Create Dockerfiles and CI/CD configurations.
- CLI Interface: Run the tool easily from the command line.

Getting Started
---------------
1. Install Dependencies:
   Run the following command to install the required packages:
       pip install -r requirements.txt

2. Set Up Environment Variables:
   Create a `.env` file in the project root with your API keys:
       OPENAI_API_KEY=your_openai_api_key
       GEMINI_API_KEY=your_gemini_api_key

3. Run the Test Generator:
   Execute the following command from the project root:
       python -m interfaces.cli --spec ./user_inputs/api_specs/petstore.yaml --test-types functional security --framework pytest --output-dir artifacts/generated_tests

Documentation
-------------
- User Guide: See docs/USER_GUIDE.md
- Developer Guide: See docs/DEVELOPER_GUIDE.md

Docker & CI/CD
--------------
This project includes a Dockerfile, a Docker Compose configuration, and GitHub Actions workflows for continuous integration.
Refer to the respective files in the project root and .github/workflows/ for more details.

License
-------
[Specify your license here]
