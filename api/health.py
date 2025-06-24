
from flask import Blueprint, jsonify
import os
import sys
import psutil
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ai-os",
        "version": "1.0.0"
    })

@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with system metrics"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "ai-os",
            "version": "1.0.0",
            "system": {
                "python_version": sys.version,
                "platform": sys.platform,
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                }
            },
            "environment": {
                "port": os.getenv('PORT', '8000'),
                "host": os.getenv('HOST', '0.0.0.0'),
                "debug": os.getenv('FLASK_ENV') == 'development'
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@health_bp.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint"""
    return "pong"

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Kubernetes-style readiness probe"""
    # Add your application-specific readiness checks here
    try:
        # Check if critical services are running
        # This is where you'd check database connections, etc.
        
        return jsonify({
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "not_ready",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 503
