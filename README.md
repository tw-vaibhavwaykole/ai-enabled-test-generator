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
**Option 1: Local Environment Setup with Python Virtual Environment**

1. **Create a Python Virtual Environment:**
   - First, clone the repository and navigate to the project root:
     ```bash
     git clone [repository-url]
     ```
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

2. **Install Dependencies:**
   - With the virtual environment activated, install the required packages:
     ```bash
     pip3 install -r requirements.txt
     ```
   - Note: If you encounter any issues, ensure you're in the project root directory where `requirements.txt` is located.

3. **Set Up Environment Variables:**
   - Create a `.env` file in the project root with your API keys:
     ```bash
     OPENAI_API_KEY=your_openai_api_key
     GEMINI_API_KEY=your_gemini_api_key
     ```

4. **Run the Test Generator with Allure Reporting:**
   ```bash
   # Generate and run tests with Allure reporting
   python3 -m interfaces.cli --spec ./api_specs/petstore.yaml --test-types functional security --framework pytest --output-dir artifacts/generated_tests
   pytest artifacts/generated_tests --alluredir=./allure-results
   allure serve ./allure-results
   ```

**Option 2: Running with Docker Compose**

1. **Ensure Docker and Docker Compose are Installed:**
   - Make sure Docker and Docker Compose are installed on your system.

2. **Build and Run the Application:**
   - From the project root, run:
     ```bash
     docker-compose up --build
     ```
   - This command uses the `docker-compose.yml` file (located in the project root) to set up the application container,
     install dependencies, and run the test generator according to the configuration in the Compose file.

Documentation
-------------
- User Guide: See docs/USER_GUIDE.md
- Developer Guide: See docs/DEVELOPER_GUIDE.md

Docker & CI/CD
--------------
This project includes a Dockerfile, a Docker Compose configuration, and GitHub Actions workflows for continuous integration.
- **Docker Compose:** Refer to the `docker-compose.yml` file in the project root for the complete configuration.
- **CI/CD Workflows:** Check the files in the `.github/workflows/` directory for GitHub Actions setups.

License
-------
[Specify your license here]

Test Reporting
-------------
This project uses Allure for test reporting. To view the reports:

1. **Install Allure:**
   - On macOS: `brew install allure`
   - On Linux: 
     ```bash
     wget https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz
     sudo tar -zxvf allure-2.24.1.tgz -C /opt/
     sudo ln -s /opt/allure-2.24.1/bin/allure /usr/bin/allure
     ```
   - On Windows: `scoop install allure`

2. **Generate and View Reports:**
   ```bash
   pytest --alluredir=./allure-results
   allure serve ./allure-results
   ```

The Allure report will open in your default web browser, showing detailed test results, including:
- Test execution statistics
- Test steps and attachments
- Failed test analysis
- Environment information
