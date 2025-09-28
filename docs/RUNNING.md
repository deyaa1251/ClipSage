# 🚀 How to Run ClipSage

## Quick Start (Recommended)

### 1. Using the Start Script
```bash
cd /home/opensource/ClipSage
./start_clipsage.sh
```

This script will automatically:
- ✅ Check dependencies
- ✅ Build the C++ clipboard manager
- ✅ Create Python virtual environment
- ✅ Install Python dependencies
- ✅ Start the clipboard monitor
- ✅ Launch the GUI application

## Manual Setup (Step by Step)

### Prerequisites
```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-venv python3-pip cmake build-essential qt6-base-dev

# Install Ollama (for semantic search)
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull all-minilm:22m
```

### Step 1: Setup Python Environment
```bash
cd /home/opensource/ClipSage

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Build C++ Clipboard Manager
```bash
cd clipsage/backend
mkdir -p build
cd build
cmake ..
make
cd ..
cp build/clipboard_manager .
```

### Step 3: Start Clipboard Manager
```bash
# Start in background
./clipboard_manager &
```

### Step 4: Run ClipSage GUI
```bash
cd /home/opensource/ClipSage
source .venv/bin/activate
python -m clipsage
```

## Alternative Running Methods

### Method 1: Direct Python Module
```bash
cd /home/opensource/ClipSage
python -m clipsage
```

### Method 2: Using __main__.py
```bash
cd /home/opensource/ClipSage
python __main__.py
```

### Method 3: Development Mode
```bash
cd /home/opensource/ClipSage
pip install -e .  # Install in development mode
clipsage           # Run as installed command
```

## Installation Script (One-time Setup)

For a complete system installation:
```bash
cd /home/opensource/ClipSage
chmod +x scripts/install.sh
./scripts/install.sh
```

This will:
- Install all system dependencies
- Set up Python environment
- Build C++ components
- Create desktop entries
- Configure auto-start (optional)

## Running in Development Mode

### For GUI Development
```bash
# Watch for changes and auto-reload
cd /home/opensource/ClipSage
source .venv/bin/activate
python -c "
import sys
sys.path.insert(0, '.')
from clipsage.gui.main_window import ClipboardManagerUI
from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)
window = ClipboardManagerUI()
window.show()
app.exec()
"
```

### For Performance Testing
```bash
cd /home/opensource/ClipSage
source .venv/bin/activate

# Run performance benchmarks
python scripts/performance_test.py

# Quick performance test
python scripts/performance_test.py quick

# Memory usage monitoring
python scripts/performance_test.py memory 5
```

## Troubleshooting

### Issue: "clipboard_manager not found"
```bash
# Build manually
cd clipsage/backend
mkdir -p build && cd build
cmake .. && make
cp clipboard_manager ..
```

### Issue: "Ollama not running"
```bash
# Start Ollama service
ollama serve &

# Pull embedding model
ollama pull all-minilm:22m

# Test Ollama
curl http://localhost:11434/api/version
```

### Issue: "PyQt6 not found"
```bash
# Install PyQt6 system-wide
sudo apt install python3-pyqt6

# Or install in virtual environment
pip install PyQt6>=6.4.0
```

### Issue: "Permission denied"
```bash
# Make scripts executable
chmod +x start_clipsage.sh
chmod +x scripts/install.sh
```

### Issue: Virtual environment problems
```bash
# Remove and recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

### Default Configuration Location
```
~/.config/clipsage/config.json
```

### Sample Configuration
```json
{
  "clipboard_path": "/tmp/clipboard_manager",
  "embedding_model": "all-minilm:22m",
  "max_items": 500,
  "refresh_interval": 15000,
  "auto_refresh": true,
  "window": {
    "width": 1200,
    "height": 800
  },
  "search": {
    "max_results": 10,
    "enable_semantic": true
  }
}
```

## Performance Optimization

### For Better Performance
```json
{
  "max_items": 300,
  "refresh_interval": 30000,
  "auto_refresh": false
}
```

### For Heavy Usage
```json
{
  "max_items": 1000,
  "refresh_interval": 10000,
  "search": {
    "max_results": 20
  }
}
```

## System Integration

### Create Desktop Entry
```bash
# Run the installation script
./scripts/install.sh

# Or manually create desktop entry
cat > ~/.local/share/applications/clipsage.desktop << EOF
[Desktop Entry]
Name=ClipSage
Comment=AI-Powered Clipboard Manager
Exec=/home/opensource/ClipSage/start_clipsage.sh
Icon=/home/opensource/ClipSage/assets/icon.png
Terminal=false
Type=Application
Categories=Utility;Office;
EOF
```

### Auto-start at Login
```bash
# Copy to autostart directory
cp ~/.local/share/applications/clipsage.desktop ~/.config/autostart/
```

## Success Indicators

When ClipSage starts successfully, you should see:
- ✅ "Clipboard manager started" message
- ✅ "Ollama service is running" confirmation
- ✅ GUI window opens with clipboard items
- ✅ Search functionality works
- ✅ No error messages in terminal

## Next Steps

After successful startup:
1. **Test search**: Type queries in the search box
2. **Check performance**: Monitor CPU/memory usage
3. **Configure settings**: Adjust refresh intervals
4. **Review logs**: Check for any error messages
5. **Test copying**: Copy text/images to see real-time updates