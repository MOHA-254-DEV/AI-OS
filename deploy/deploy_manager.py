
import os
import subprocess
import shutil
import json
import sys
from pathlib import Path

class DeployManager:
    def __init__(self):
        self.project_dir = os.getcwd()
        self.required_files = ["requirements.txt", "main.py", "aios.py"]
        
    def check_requirements(self):
        """Check if all required files exist"""
        missing_files = []
        for file in self.required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
        
        print("✅ All required files present")
        return True

    def deploy_to_replit(self):
        """Deploy to Replit"""
        print("[DEPLOY] Replit: Setting up .replit configuration...")
        
        replit_config = '''run = "python main.py"
language = "python3"
entrypoint = "main.py"

[nix]
channel = "stable-23.05"

[deployment]
run = ["sh", "-c", "python main.py"]
deploymentTarget = "cloudrun"

[[ports]]
localPort = 8000
externalPort = 80
'''
        
        with open(".replit", "w") as f:
            f.write(replit_config)
            
        # Ensure main.py exists as entry point
        if not os.path.exists("main.py") and os.path.exists("aios.py"):
            shutil.copy("aios.py", "main.py")
            
        print("✅ Replit deployment configured")

    def deploy_to_render(self):
        """Deploy to Render.com"""
        print("[DEPLOY] Render: Creating render.yaml...")
        
        render_config = {
            "services": [
                {
                    "type": "web",
                    "name": "ai-os",
                    "env": "python",
                    "buildCommand": "pip install -r requirements.txt",
                    "startCommand": "python main.py",
                    "plan": "free",
                    "region": "oregon",
                    "branch": "main",
                    "healthCheckPath": "/health",
                    "envVars": [
                        {
                            "key": "PYTHON_VERSION",
                            "value": "3.11.0"
                        },
                        {
                            "key": "PORT",
                            "value": "10000"
                        }
                    ]
                }
            ]
        }
        
        with open("render.yaml", "w") as f:
            json.dump(render_config, f, indent=2)
            
        print("✅ Render deployment config created")

    def deploy_to_railway(self):
        """Deploy to Railway"""
        print("[DEPLOY] Railway: Creating railway.json...")
        
        railway_config = {
            "$schema": "https://railway.app/railway.schema.json",
            "build": {
                "builder": "NIXPACKS",
                "buildCommand": "pip install -r requirements.txt"
            },
            "deploy": {
                "startCommand": "python main.py",
                "healthcheckPath": "/health",
                "healthcheckTimeout": 100,
                "restartPolicyType": "ON_FAILURE"
            }
        }
        
        with open("railway.json", "w") as f:
            json.dump(railway_config, f, indent=2)
            
        print("✅ Railway deployment config created")

    def deploy_to_heroku(self):
        """Deploy to Heroku"""
        print("[DEPLOY] Heroku: Creating Procfile and runtime.txt...")
        
        # Create Procfile
        with open("Procfile", "w") as f:
            f.write("web: python main.py\n")
            
        # Create runtime.txt
        with open("runtime.txt", "w") as f:
            f.write("python-3.11.7\n")
            
        # Create app.json for Heroku Button
        app_config = {
            "name": "AI Operating System",
            "description": "Autonomous AI Operating System with multi-agent capabilities",
            "repository": "https://github.com/yourusername/ai-os",
            "keywords": ["python", "ai", "agents", "automation"],
            "env": {
                "FLASK_ENV": {
                    "description": "Flask environment",
                    "value": "production"
                },
                "PORT": {
                    "description": "Port to run the application on",
                    "value": "5000"
                }
            },
            "formation": {
                "web": {
                    "quantity": 1,
                    "size": "basic"
                }
            }
        }
        
        with open("app.json", "w") as f:
            json.dump(app_config, f, indent=2)
            
        print("✅ Heroku deployment files created")

    def deploy_to_fly_io(self):
        """Deploy to Fly.io"""
        print("[DEPLOY] Fly.io: Creating fly.toml...")
        
        fly_config = '''app = "ai-os"
primary_region = "ord"

[build]
  [build.env]
    PYTHONPATH = "/app"

[env]
  PORT = "8080"
  PYTHONUNBUFFERED = "1"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
'''
        
        with open("fly.toml", "w") as f:
            f.write(fly_config)
            
        print("✅ Fly.io deployment config created")

    def create_dockerfile(self):
        """Create optimized Dockerfile"""
        print("[DEPLOY] Creating production Dockerfile...")
        
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "main.py"]
'''
        
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
            
        # Create .dockerignore
        dockerignore_content = '''__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
.git/
.gitignore
README.md
.env
.venv/
venv/
.pytest_cache/
.coverage
htmlcov/
.DS_Store
*.log
logs/
'''
        
        with open(".dockerignore", "w") as f:
            f.write(dockerignore_content)
            
        print("✅ Docker files created")

    def create_github_actions(self):
        """Create GitHub Actions workflow"""
        print("[DEPLOY] Creating GitHub Actions workflow...")
        
        os.makedirs(".github/workflows", exist_ok=True)
        
        workflow_content = '''name: Deploy AI OS

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Build and push Docker image
      if: github.event_name == 'push'
      run: |
        echo "Docker build would happen here"
        # docker build -t ai-os:latest .
        # docker push ai-os:latest
'''
        
        with open(".github/workflows/deploy.yml", "w") as f:
            f.write(workflow_content)
            
        print("✅ GitHub Actions workflow created")

    def deploy_all_platforms(self):
        """Deploy to all supported platforms"""
        if not self.check_requirements():
            return False
            
        print("🚀 Starting multi-platform deployment setup...")
        
        self.deploy_to_replit()
        self.deploy_to_render()
        self.deploy_to_railway()
        self.deploy_to_heroku()
        self.deploy_to_fly_io()
        self.create_dockerfile()
        self.create_github_actions()
        
        print("\n✅ Multi-platform deployment files created successfully!")
        print("\nPlatform-specific instructions:")
        print("📱 Replit: Push to Replit and click Deploy")
        print("🎨 Render: Connect GitHub repo to Render dashboard")
        print("🚂 Railway: Connect GitHub repo to Railway")
        print("💜 Heroku: git push heroku main")
        print("🪰 Fly.io: fly deploy")
        print("🐳 Docker: docker build -t ai-os . && docker run -p 8000:8000 ai-os")
        
        return True

if __name__ == "__main__":
    deployer = DeployManager()
    deployer.deploy_all_platforms()
