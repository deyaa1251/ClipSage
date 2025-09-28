# ClipSage Installation Guide

This guide covers different installation methods for ClipSage.

## Quick Installation

### Automated Installation (Recommended)

```bash
git clone https://github.com/clipsage/clipsage.git
cd clipsage
chmod +x scripts/install.sh
./scripts/install.sh
```

This will:
- Check system requirements
- Install Python dependencies
- Build the C++ backend
- Install and configure Ollama
- Create desktop entries and launchers

### Manual Installation

1. **Install System Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv cmake build-essential qt6-base-dev
   ```

2. **Clone and Setup:**
   ```bash
   git clone https://github.com/clipsage/clipsage.git
   cd clipsage
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Build Backend:**
   ```bash
   cd clipsage/backend
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release
   make -j$(nproc)
   cp clipboard_manager ..
   ```

4. **Install Ollama:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama serve &
   ollama pull all-minilm:22m
   ```

## Package Installation

### Snap Package
```bash
sudo snap install clipsage
```

### Debian Package
```bash
wget https://github.com/clipsage/clipsage/releases/latest/download/clipsage_1.0.0_amd64.deb
sudo dpkg -i clipsage_1.0.0_amd64.deb
sudo apt-get install -f  # Fix dependencies if needed
```

### AppImage
```bash
wget https://github.com/clipsage/clipsage/releases/latest/download/ClipSage-1.0.0-x86_64.AppImage
chmod +x ClipSage-1.0.0-x86_64.AppImage
./ClipSage-1.0.0-x86_64.AppImage
```

## Development Installation

For developers who want to contribute:

```bash
git clone https://github.com/clipsage/clipsage.git
cd clipsage
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]  # Install with development dependencies
```

## Verification

After installation, verify everything works:

```bash
# Check if ClipSage can be imported
python -c "import clipsage; print('✅ ClipSage installed successfully')"

# Check backend
clipsage --help

# Run tests
python -m pytest tests/
```

## Troubleshooting

### Common Issues

1. **Qt6 Not Found:**
   ```bash
   sudo apt install qt6-base-dev qt6-tools-dev
   ```

2. **CMake Errors:**
   ```bash
   sudo apt install cmake build-essential
   ```

3. **Ollama Not Working:**
   ```bash
   # Check if Ollama is running
   pgrep ollama
   
   # Start Ollama if not running
   ollama serve &
   
   # Pull the model
   ollama pull all-minilm:22m
   ```

4. **Permission Issues:**
   ```bash
   # Make sure /tmp/clipboard_manager is writable
   ls -la /tmp/clipboard_manager
   
   # Fix permissions if needed
   chmod 755 /tmp/clipboard_manager
   ```

## Uninstallation

### Remove ClipSage
```bash
# Stop processes
pkill -f clipboard_manager
pkill -f clipsage

# Remove installation
sudo rm -f /usr/local/bin/clipsage
rm -rf ~/.config/clipsage
rm -rf ~/.local/share/applications/clipsage.desktop

# Remove data (optional)
rm -rf /tmp/clipboard_manager
```

### Remove Snap
```bash
sudo snap remove clipsage
```

### Remove Debian Package
```bash
sudo apt remove clipsage
```