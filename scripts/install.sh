#!/bin/bash

# ClipSage Installation Script
# This script handles the complete installation of ClipSage

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🚀 ClipSage Installation Script"
echo "================================="

# Check system requirements
check_requirements() {
    echo "📋 Checking system requirements..."
    
    # Check for Python 3.12+
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is required but not installed"
        exit 1
    fi
    
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo "✅ Python $python_version found"
    
    # Check for CMake
    if ! command -v cmake &> /dev/null; then
        echo "❌ CMake is required but not installed"
        echo "   Install with: sudo apt install cmake"
        exit 1
    fi
    echo "✅ CMake found"
    
    # Check for Qt6 development libraries
    if ! pkg-config --exists Qt6Core; then
        echo "⚠️  Qt6 development libraries not found"
        echo "   Install with: sudo apt install qt6-base-dev qt6-tools-dev"
        echo "   Continuing anyway..."
    else
        echo "✅ Qt6 development libraries found"
    fi
    
    # Check for GCC/Clang
    if ! command -v g++ &> /dev/null && ! command -v clang++ &> /dev/null; then
        echo "❌ C++ compiler (g++ or clang++) is required"
        echo "   Install with: sudo apt install build-essential"
        exit 1
    fi
    echo "✅ C++ compiler found"
}

# Install Python dependencies
install_python_deps() {
    echo "🐍 Installing Python dependencies..."
    
    cd "$PROJECT_ROOT"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d ".venv" ]; then
        echo "   Creating virtual environment..."
        python3 -m venv .venv
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install dependencies
    echo "   Installing Python packages..."
    pip install --upgrade pip
    
    # Install from pyproject.toml if it exists, otherwise from requirements
    if [ -f "pyproject.toml" ]; then
        pip install -e .
    elif [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo "   Installing basic dependencies..."
        pip install PyQt6 langchain langchain-ollama pillow
    fi
    
    echo "✅ Python dependencies installed"
}

# Build C++ clipboard manager
build_backend() {
    echo "🔨 Building C++ clipboard manager..."
    
    backend_dir="$PROJECT_ROOT/clipsage/backend"
    cd "$backend_dir"
    
    # Create build directory
    mkdir -p build
    cd build
    
    # Configure and build
    echo "   Configuring CMake..."
    cmake .. -DCMAKE_BUILD_TYPE=Release
    
    echo "   Building..."
    make -j$(nproc)
    
    # Copy binary to backend directory
    if [ -f "clipboard_manager" ]; then
        cp clipboard_manager ..
        echo "✅ Clipboard manager built successfully"
    else
        echo "❌ Failed to build clipboard manager"
        exit 1
    fi
    
    cd "$PROJECT_ROOT"
}

# Install Ollama if not present
install_ollama() {
    echo "🤖 Checking Ollama installation..."
    
    if command -v ollama &> /dev/null; then
        echo "✅ Ollama is already installed"
    else
        echo "   Installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
    
    # Check if service is running
    if ! pgrep -f "ollama serve" > /dev/null; then
        echo "   Starting Ollama service..."
        ollama serve &
        sleep 3
    fi
    
    # Pull the embedding model
    echo "   Pulling embedding model..."
    ollama pull all-minilm:22m
    
    echo "✅ Ollama setup complete"
}

# Create desktop entry
create_desktop_entry() {
    echo "🖥️  Creating desktop entry..."
    
    desktop_dir="$HOME/.local/share/applications"
    mkdir -p "$desktop_dir"
    
    cat > "$desktop_dir/clipsage.desktop" << EOF
[Desktop Entry]
Name=ClipSage
Comment=Advanced Clipboard Manager with Semantic Search
Exec=$PROJECT_ROOT/scripts/clipsage.sh
Icon=$PROJECT_ROOT/assets/icon.png
Type=Application
Categories=Utility;Office;
StartupNotify=true
EOF
    
    echo "✅ Desktop entry created"
}

# Create launcher script
create_launcher() {
    echo "📝 Creating launcher script..."
    
    scripts_dir="$PROJECT_ROOT/scripts"
    mkdir -p "$scripts_dir"
    
    cat > "$scripts_dir/clipsage.sh" << 'EOF'
#!/bin/bash

# ClipSage Launcher Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment
source "$PROJECT_ROOT/.venv/bin/activate"

# Start ClipSage
cd "$PROJECT_ROOT"
python -m clipsage
EOF
    
    chmod +x "$scripts_dir/clipsage.sh"
    
    # Create symlink in /usr/local/bin if possible
    if [ -w "/usr/local/bin" ] || sudo -n true 2>/dev/null; then
        echo "   Creating system-wide launcher..."
        sudo ln -sf "$scripts_dir/clipsage.sh" /usr/local/bin/clipsage
    fi
    
    echo "✅ Launcher script created"
}

# Main installation process
main() {
    check_requirements
    install_python_deps
    build_backend
    install_ollama
    create_launcher
    create_desktop_entry
    
    echo ""
    echo "🎉 ClipSage installation completed successfully!"
    echo ""
    echo "To start ClipSage:"
    echo "  • Run: $PROJECT_ROOT/scripts/clipsage.sh"
    echo "  • Or: clipsage (if system-wide launcher was created)"
    echo "  • Or: Search for 'ClipSage' in your application menu"
    echo ""
    echo "Configuration is stored in: ~/.config/clipsage/"
    echo "Clipboard data is stored in: /tmp/clipboard_manager/"
}

# Handle command line arguments
case "${1:-install}" in
    "install")
        main
        ;;
    "check")
        check_requirements
        ;;
    "python")
        install_python_deps
        ;;
    "backend")
        build_backend
        ;;
    "ollama")
        install_ollama
        ;;
    *)
        echo "Usage: $0 [install|check|python|backend|ollama]"
        echo "  install - Full installation (default)"
        echo "  check   - Check system requirements only"
        echo "  python  - Install Python dependencies only"
        echo "  backend - Build C++ backend only"
        echo "  ollama  - Install/setup Ollama only"
        exit 1
        ;;
esac