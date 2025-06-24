# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Run the main application
python main.py
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Run the main application
python main.py
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -e .
# Or for development:
pip install -e ".[dev]"
setup(
    name="ai_os",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<1.0.0",
        "uvicorn>=0.15.0,<1.0.0",
        "speechrecognition>=3.8.1,<4.0.0",
        "pyaudio>=0.2.11,<1.0.0",
        "pyppeteer>=1.0.2,<2.0.0",
        "beautifulsoup4>=4.9.3,<5.0.0",
        "cryptography>=35.0.0,<36.0.0",
        "openai-whisper==20231117"
    ],
    python_requires=">=3.8",
    author="AI OS Team",
    description="An AI-powered operating system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
setup(
    name="ai_os",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<1.0.0",
        "uvicorn>=0.15.0,<1.0.0",
        "speechrecognition>=3.8.1,<4.0.0",
        "pyaudio>=0.2.11,<1.0.0",
        "pyppeteer>=1.0.2,<2.0.0",
        "beautifulsoup4>=4.9.3,<5.0.0",
        "cryptography>=35.0.0,<36.0.0",
        "openai-whisper==20231117"
    ],
    python_requires=">=3.8",
    author="AI OS Team",
    description="An AI-powered operating system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -e .
# Or for development:
pip install -e ".[dev]"
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Install dependencies
pip install -e .
# Or for development:
pip install -e ".[dev]"
setup(
    name="ai_os",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<1.0.0",
        "uvicorn>=0.15.0,<1.0.0",
        "speechrecognition>=3.8.1,<4.0.0",
        "pyaudio>=0.2.11,<1.0.0",
        "pyppeteer>=1.0.2,<2.0.0",
        "beautifulsoup4>=4.9.3,<5.0.0",
        "cryptography>=35.0.0,<36.0.0",
        "openai-whisper==20231117"
    ],
    python_requires=">=3.8",
    author="AI OS Team",
    description="An AI-powered operating system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
setup(
    name="ai_os",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<1.0.0",
        "uvicorn>=0.15.0,<1.0.0",
        "speechrecognition>=3.8.1,<4.0.0",
        "pyaudio>=0.2.11,<1.0.0",
        "pyppeteer>=1.0.2,<2.0.0",
        "beautifulsoup4>=4.9.3,<5.0.0",
        "cryptography>=35.0.0,<36.0.0",
        "openai-whisper==20231117"
    ],
    python_requires=">=3.8",
    author="AI OS Team",
    description="An AI-powered operating system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
import subprocess

class DependencyResolver:
    def __init__(self):
        pass

    def install_requirements_txt(self, path):
        req_file = os.path.join(path, 'requirements.txt')
        if os.path.exists(req_file):
            print("📦 Installing requirements.txt...")
            subprocess.run(['pip', 'install', '-r', req_file])

    def install_pyproject(self, path):
        py_file = os.path.join(path, 'pyproject.toml')
        if os.path.exists(py_file):
            print("📦 Installing pyproject.toml dependencies...")
            subprocess.run(['pip', 'install', path])

    def install_dependencies(self, path):
        self.install_requirements_txt(path)
        self.install_pyproject(path)
