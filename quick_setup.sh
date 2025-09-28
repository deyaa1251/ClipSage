#!/bin/bash

# Quick Setup Script for ClipSage
echo "🚀 ClipSage Quick Setup"
echo "======================"

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python3 first:"
    echo "   sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install basic dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install PyQt6>=6.4.0 langchain>=0.2.0 langchain-ollama>=0.1.0 Pillow>=9.0.0 httpx>=0.25.0 psutil>=5.9.0

# Test import
echo "🧪 Testing ClipSage import..."
if python3 -c "import clipsage; print('✅ ClipSage ready!')"; then
    echo ""
    echo "✅ Setup complete! You can now run ClipSage:"
    echo ""
    echo "   ./start_clipsage.sh"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Install and start Ollama: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   2. Pull embedding model: ollama pull all-minilm:22m"
    echo "   3. Start Ollama service: ollama serve &"
    echo "   4. Run ClipSage: ./start_clipsage.sh"
else
    echo "❌ Setup failed. Check error messages above."
    exit 1
fi