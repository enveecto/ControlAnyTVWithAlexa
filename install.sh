#!/usr/bin/env bash
set -e

echo "=== Installing ControlAnyTVWithAlexa ==="

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required. Please install python3."
    exit 1
fi

# Check ADB
if ! command -v adb &> /dev/null; then
    echo "Notice: adb binary not found in PATH. You can install adb (apt install adb / brew install android-platform-tools) or specify adb_path in config.json."
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Install dependencies
echo "Installing Python dependencies..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Create config.json if not present
if [ ! -f "config.json" ]; then
    cp config.example.json config.json
    echo "Created config.json from template. Please edit config.json with your Sinric Pro keys & TV IP."
fi

echo "=== Installation Complete! ==="
echo "Run the bridge with: ./venv/bin/python bridge.py"
