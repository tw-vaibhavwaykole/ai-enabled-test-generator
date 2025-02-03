# ai-test-generator/generators/infrastructure/docker_generator.py

class DockerGenerator:
    """
    Generates a Dockerfile based on provided configuration parameters.
    """

    def __init__(self, base_image: str = "python:3.8-slim", workdir: str = "/app", requirements_file: str = "requirements.txt"):
        """
        :param base_image: The base Docker image to use.
        :param workdir: The working directory inside the container.
        :param requirements_file: Path to the requirements file.
        """
        self.base_image = base_image
        self.workdir = workdir
        self.requirements_file = requirements_file

    def generate_dockerfile(self) -> str:
        """
        Generates Dockerfile content as a string.
        """
        dockerfile_lines = [
            f"FROM {self.base_image}",
            f"WORKDIR {self.workdir}",
            "COPY . .",
            f"RUN pip install --no-cache-dir -r {self.requirements_file}",
            "EXPOSE 8000",
            'CMD ["python", "-m", "interfaces.cli"]'
        ]
        return "\n".join(dockerfile_lines)

    def save_dockerfile(self, output_path: str) -> None:
        """
        Saves the generated Dockerfile content to the specified output path.
        
        :param output_path: Path to save the Dockerfile.
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(self.generate_dockerfile())
            print(f"Dockerfile generated at: {output_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to generate Dockerfile: {e}") from e


# --- Example Usage ---
# if __name__ == "__main__":
#     docker_gen = DockerGenerator()
#     docker_gen.save_dockerfile("Dockerfile")
