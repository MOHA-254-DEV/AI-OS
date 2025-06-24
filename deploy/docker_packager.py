class DockerPackager:
    def __init__(self):
        self.dockerfile = """
FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "aios.py"]
"""

    def write_dockerfile(self, path="Dockerfile"):
        with open(path, "w") as f:
            f.write(self.dockerfile.strip())
        print("[DOCKER] Dockerfile created.")

    def build_image(self, tag="aios:latest"):
        os.system(f"docker build -t {tag} .")

    def run_container(self, tag="aios:latest"):
        os.system(f"docker run -p 8080:8000 {tag}")

if __name__ == "__main__":
    docker = DockerPackager()
    docker.write_dockerfile()
    docker.build_image()
