
#!/bin/bash

# AI OS Start Script
echo "🚀 Starting AI Operating System..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python_version"

# Install dependencies if needed
if [ ! -f ".deps_installed" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch .deps_installed
fi

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export FLASK_ENV=${FLASK_ENV:-production}
export PORT=${PORT:-8000}
export HOST=${HOST:-0.0.0.0}

# Start the application
echo "🎯 Starting on $HOST:$PORT"
python3 main.py
