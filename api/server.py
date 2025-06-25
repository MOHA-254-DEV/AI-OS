from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import datetime

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    CORS(app, origins=["*"])

    # In-memory storage for demonstration (replace with DB for production)
    app.agents = []
    app.tasks = []

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
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

    # AGENTS ENDPOINTS (CRUD)
    @app.route("/api/v1/agents", methods=["GET", "POST", "DELETE"])
    def agents():
        if request.method == "GET":
            return jsonify({"agents": app.agents})
        elif request.method == "POST":
            data = request.get_json()
            name = data.get("name", "").strip()
            if not name:
                return jsonify({"error": "Name required"}), 400
            new_agent = {
                "id": len(app.agents) + 1,
                "name": name,
                "status": "idle"
            }
            app.agents.append(new_agent)
            return jsonify({"success": True, "agent": new_agent}), 201
        elif request.method == "DELETE":
            agent_id = int(request.args.get("id", "0"))
            before = len(app.agents)
            app.agents = [a for a in app.agents if a["id"] != agent_id]
            if len(app.agents) == before:
                return jsonify({"error": "Agent not found"}), 404
            return jsonify({"success": True})

    # TASKS ENDPOINTS (CRUD)
    @app.route("/api/v1/tasks", methods=["GET", "POST", "DELETE"])
    def tasks():
        if request.method == "GET":
            return jsonify({"tasks": app.tasks})
        elif request.method == "POST":
            data = request.get_json()
            desc = data.get("description", "").strip()
            if not desc:
                return jsonify({"error": "Description required"}), 400
            new_task = {
                "id": len(app.tasks) + 1,
                "description": desc,
                "status": "pending"
            }
            app.tasks.append(new_task)
            return jsonify({"success": True, "task": new_task}), 201
        elif request.method == "DELETE":
            task_id = int(request.args.get("id", "0"))
            before = len(app.tasks)
            app.tasks = [t for t in app.tasks if t["id"] != task_id]
            if len(app.tasks) == before:
                return jsonify({"error": "Task not found"}), 404
            return jsonify({"success": True})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()
