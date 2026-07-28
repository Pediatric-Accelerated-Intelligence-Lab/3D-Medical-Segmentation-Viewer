#!/usr/bin/env bash

set -e

ENV_DIR=".venv"

if ! command -v python3.11 >/dev/null 2>&1; then
    echo "Error: Python 3.11 is required but was not found."
    exit 1
fi

if [ ! -d "$ENV_DIR" ]; then
    echo "Creating Python virtual environment..."
    python3.11 -m venv "$ENV_DIR"
    
    echo "Activating the virtual environment..."
    source "$ENV_DIR/bin/activate"

    echo "Installing Python dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
fi

echo "Activating the virtual environment..."
source "$ENV_DIR/bin/activate"

echo "Starting deployment..."
python app.py
