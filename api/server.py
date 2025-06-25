from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    CORS(app, origins=["*"])

    # In-memory storage for demo purposes
    app.agents = []
    app.tasks = []

    @app.route("/")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    @app.route("/api/v1/status")
    def api_status():
        return jsonify({
            "api_version": "1.0.0",
            "features": ["voice_commands", "task_management", "agent_coordination"],
            "status": "operational"
        })

    # AGENTS ENDPOINTS
    @app.route("/api/v1/agents", methods=["GET", "POST", "DELETE"])
    def agents():
        if request.method == "GET":
            return jsonify({"agents": app.agents})
        elif request.method == "POST":
            data = request.get_json()
            new_agent = {
                "id": len(app.agents) + 1,
                "name": data.get("name", f"Agent {len(app.agents)+1}"),
                "status": "idle"
            }
            app.agents.append(new_agent)
            return jsonify({"success": True, "agent": new_agent}), 201
        elif request.method == "DELETE":
            agent_id = int(request.args.get("id", "0"))
            app.agents = [a for a in app.agents if a["id"] != agent_id]
            return jsonify({"success": True})

    # TASKS ENDPOINTS
    @app.route("/api/v1/tasks", methods=["GET", "POST", "DELETE"])
    def tasks():
        if request.method == "GET":
            return jsonify({"tasks": app.tasks})
        elif request.method == "POST":
            data = request.get_json()
            new_task = {
                "id": len(app.tasks) + 1,
                "description": data.get("description", f"Task {len(app.tasks)+1}"),
                "status": "pending"
            }
            app.tasks.append(new_task)
            return jsonify({"success": True, "task": new_task}), 201
        elif request.method == "DELETE":
            task_id = int(request.args.get("id", "0"))
            app.tasks = [t for t in app.tasks if t["id"] != task_id]
            return jsonify({"success": True})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()
