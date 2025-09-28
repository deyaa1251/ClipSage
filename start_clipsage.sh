#!/bin/bash

# ClipSage Startup Script
# This script starts both the clipboard manager and the GUI application

echo "🚀 Starting ClipSage - Advanced Clipboard Manager"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "src/app/main.py" ]; then
    echo "Error: Please run this script from the ClipSage root directory"
    exit 1
fi

# Check if clipboard manager is running
if ! pgrep -f "clipboard_manager" > /dev/null; then
    echo " Clipboard manager not running. Starting it now..."
    cd src/clip_board
    
    # Build if necessary
    if [ ! -f "build/clipboard_manager" ]; then
        echo " Building clipboard manager..."
        ./install.sh
    fi
    
    # Start clipboard manager in background
    echo " Starting clipboard manager..."
    ./run_clipboard_manager.sh &
    CLIPBOARD_PID=$!
    cd ../../
    
    # Wait a moment for it to start
    sleep 2
    
    echo " Clipboard manager started (PID: $CLIPBOARD_PID)"
else
    echo "Clipboard manager already running"
fi

# Check Python environment
echo " Checking Python environment..."
cd src/app

if [ ! -d ".venv" ]; then
    echo "️  Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo " Virtual environment found"
fi

# Check if Ollama is running
if ! pgrep -f "ollama" > /dev/null; then
    echo "️Ollama not running. Please start Ollama service first:"
    echo "   ollama serve"
    echo "   ollama pull all-minilm:22m"
    echo ""
    echo "Continuing anyway - semantic search may not work..."
else
    echo " Ollama service is running"
fi

# Start the GUI application
echo " ClipSage GUI..."
echo "=================================================="

# Activate virtual environment and run
source .venv/bin/activate
python clipsage.py

echo ""
echo " ClipSage session ended"