from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.auth import token_required
from api.health import health_bp
import logging
import os

def create_app():
    app = Flask(__name__)

    # Enable CORS for all domains
    CORS(app)

    # Register blueprints
    app.register_blueprint(health_bp)

    logger = logging.getLogger(__name__)

    @app.route('/api/test', methods=['GET'])
    @token_required
    def test_endpoint(current_user):
        return jsonify({"message": "API is working", "user": current_user})

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "message": "AI Operating System API",
            "version": "1.0.0",
            "status": "running"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)