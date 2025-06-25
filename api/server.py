
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__)
    CORS(app, origins=["*"])

    @app.route("/")
    def home():
        return jsonify({
            "status": "running",
            "service": "AI Operating System",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "api": "/api/v1"
            }
        })

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z"
        })

    @app.route("/api/v1/status")
    def api_status():
        return jsonify({
            "api_version": "1.0.0",
            "features": [
                "voice_commands",
                "task_management",
                "agent_coordination"
            ],
            "status": "operational"
        })

    return app
            "features": ["voice_commands", "task_management", "agent_coordination"],
            "status": "operational"
        })
    
    return app</new_str>
