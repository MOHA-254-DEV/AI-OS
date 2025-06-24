from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from .analytics_engine import AnalyticsEngine
import logging
import os
import sys

app = Flask(__name__)
CORS(app)

engine = AnalyticsEngine()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

@app.route("/api/metrics")
def metrics():
    try:
        result = engine.analyze()
        return jsonify(result)
    except Exception as e:
        logger.exception("Error while fetching metrics")
        return jsonify({"error": "Failed to fetch metrics"}), 500

@app.route("/")
def dashboard():
    try:
        return send_from_directory("static", "dashboard.html", mimetype="text/html")
    except Exception as e:
        logger.exception("Error loading dashboard")
        return jsonify({"error": "Failed to load dashboard"}), 500

@app.route("/shutdown", methods=["POST"])
def shutdown():
    """
    Gracefully shuts down the Flask server.
    """
    logger.info("Shutdown signal received.")
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        logger.warning("Shutdown not available.")
        return jsonify({"error": "Not running with the Werkzeug Server"}), 500
    func()
    return jsonify({"message": "Server shutting down..."}), 200

@app.before_first_request
def prepopulate_data():
    """
    Populate example metrics before first request.
    """
    try:
        engine.log_task("agent-A", "email_parse", "success")
        engine.log_task("agent-B", "data_scrape", "failure")
        engine.log_task("agent-A", "report_generate", "success")
        engine.log_error("agent-B", "timeout_error")
        logger.info("Sample data prepopulated.")
    except Exception as e:
        logger.exception("Error prepopulating sample data")

if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 5001))
        logger.info(f"Starting Flask server on port {port}")
        app.run(host="0.0.0.0", port=port, debug=True)
    except KeyboardInterrupt:
        logger.info("Server interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception("Failed to start Flask server")
        sys.exit(1)
