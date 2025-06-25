
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
            "timestamp": "2025-06-25T12:39:17Z"
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

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app
