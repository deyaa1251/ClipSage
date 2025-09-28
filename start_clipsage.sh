#!/bin/bash

# ClipSage Startup Script
# This script starts both the clipboard manager and the GUI application

echo "🚀 Starting ClipSage - Advanced Clipboard Manager"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "clipsage" ]; then
    echo "❌ Error: Please run this script from the ClipSage root directory"
    echo "   Expected: pyproject.toml and clipsage/ directory"
    exit 1
fi

# Check if clipboard manager is running
if ! pgrep -f "clipboard_manager" > /dev/null; then
    echo "📋 Clipboard manager not running. Starting it now..."
    cd clipsage/backend
    
    # Build if necessary
    if [ ! -f "clipboard_manager" ]; then
        echo "🔨 Building clipboard manager..."
        mkdir -p build
        cd build
        cmake ..
        make
        cd ..
        # Copy binary to backend directory
        cp build/clipboard_manager . 2>/dev/null || echo "⚠️  Build may have failed"
    fi
    
    # Start clipboard manager in background
    if [ -f "clipboard_manager" ]; then
        echo "🚀 Starting clipboard manager..."
        ./clipboard_manager &
        CLIPBOARD_PID=$!
        echo "✅ Clipboard manager started (PID: $CLIPBOARD_PID)"
    else
        echo "⚠️  Clipboard manager binary not found, continuing anyway..."
    fi
    
    cd ../../
    
    # Wait a moment for it to start
    sleep 2
else
    echo "✅ Clipboard manager already running"
fi

# Check Python environment
echo "🐍 Checking Python environment..."

if [ ! -d ".venv" ]; then
    echo "🔧 Virtual environment not found. Creating one..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
    source .venv/bin/activate
fi

# Check if Ollama is running
if ! pgrep -f "ollama" > /dev/null; then
    echo "🤖 Ollama not running. Please start Ollama service first:"
    echo "   ollama serve"
    echo "   ollama pull all-minilm:22m"
    echo ""
    echo "⚠️  Continuing anyway - semantic search may not work..."
else
    echo "✅ Ollama service is running"
fi

# Start the GUI application
echo "🎨 Starting ClipSage GUI..."
echo "=================================================="

# Run the application using the new modular structure
python -m clipsage

echo ""
echo "✅ ClipSage session ended"