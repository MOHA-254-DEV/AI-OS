import os
import json
from utils.logger import logger


class FullStackAgent:
    def __init__(self, base_path="generated_apps"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def generate_app(self, name: str, stack: str = "react-flask") -> dict:
        app_dir = os.path.join(self.base_path, name)
        frontend_dir = os.path.join(app_dir, "frontend")
        backend_dir = os.path.join(app_dir, "backend")

        os.makedirs(frontend_dir, exist_ok=True)
        os.makedirs(backend_dir, exist_ok=True)

        if "react" in stack:
            self._init_react(frontend_dir)
        if "flask" in stack:
            self._init_flask(backend_dir)

        logger.info(f"{stack} app scaffolded at {app_dir}")
        return {"status": "success", "app": name, "stack": stack, "path": app_dir}

    def _init_react(self, path: str):
        files = {
            "App.jsx": """import React from 'react';
export default function App() {
  return <h1>Hello from React</h1>;
}
""",
            "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>React App</title>
</head>
<body>
  <div id="root"></div>
  <script src="index.js" type="module"></script>
</body>
</html>
""",
            "index.js": """import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);
"""
        }

        for filename, content in files.items():
            with open(os.path.join(path, filename), "w") as f:
                f.write(content)

    def _init_flask(self, path: str):
        files = {
            "app.py": """from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {"message": "Hello from Flask"}

if __name__ == '__main__':
    app.run(debug=True)
""",
            "Dockerfile": """FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask flask-cors
CMD ["python", "app.py"]
"""
        }

        for filename, content in files.items():
            with open(os.path.join(path, filename), "w") as f:
                f.write(content)

    def build_crud(self, name: str, model: str) -> dict:
        """
        Builds a simple in-memory CRUD Flask API for the given model.
        """
        crud_path = os.path.join(self.base_path, name, "backend", "crud.py")
        fields = [f.strip() for f in model.split(",") if f.strip()]

        crud_code = f"""from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

items = []

@app.route('/items', methods=['GET'])
def list_items():
    return jsonify(items), 200

@app.route('/items', methods=['POST'])
def create_item():
    item = request.get_json()
    if not isinstance(item, dict):
        return {{'error': 'Invalid item'}}, 400
    items.append(item)
    return item, 201

@app.route('/items/<int:idx>', methods=['PUT'])
def update_item(idx):
    if idx >= len(items):
        return {{'error': 'Item not found'}}, 404
    updated = request.get_json()
    items[idx] = updated
    return updated, 200

@app.route('/items/<int:idx>', methods=['DELETE'])
def delete_item(idx):
    if idx >= len(items):
        return {{'error': 'Item not found'}}, 404
    removed = items.pop(idx)
    return removed, 200

if __name__ == '__main__':
    app.run(debug=True)
"""
        with open(crud_path, "w") as f:
            f.write(crud_code)

        logger.info("CRUD Flask API generated.")
        return {"status": "success", "crud_file": crud_path, "fields": fields}

    def deploy_stack(self, name: str) -> dict:
        """
        Stub for simulating deployment of app.
        """
        logger.info(f"Simulating deployment of app '{name}'...")
        return {
            "status": "deployed",
            "url": f"http://localhost:5000/{name}",
            "message": "Deployment simulated. Add real CI/CD or Docker deployment here."
        }
