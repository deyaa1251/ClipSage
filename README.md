# ClipSage - Advanced Clipboard Manager with Semantic Search

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Qt6](https://img.shields.io/badge/Qt-6.0+-green.svg)](https://www.qt.io/)

ClipSage is a modern, intelligent clipboard manager that combines semantic search capabilities with a sleek PyQt6 interface. It automatically captures and indexes your clipboard history, enabling AI-powered search through your copied content.

## ✨ Features

### 🔍 **Intelligent Search**
- **Semantic Search**: Find content by meaning, not just keywords
- **AI-Powered**: Uses Ollama embeddings (all-minilm:22m model)
- **Real-time Results**: Instant search with live preview
- **Context Aware**: Understands relationships between different content types

### 📋 **Smart Clipboard Management**
- **Automatic Capture**: Monitors system clipboard in real-time
- **Content Types**: Supports text and images with automatic classification
- **Persistent Storage**: Reliable storage with organized file structure
- **Background Monitoring**: Efficient C++ backend for system-wide capture

### 🎨 **Modern Interface**
- **Clean Design**: Modern PyQt6 interface with intuitive navigation
- **Live Preview**: Real-time content preview and details
- **Configurable**: Customizable settings and preferences
- **Cross-platform**: Linux support with desktop integration

## 🏗️ Architecture

ClipSage follows a modular architecture with clear separation of concerns:

```
clipsage/
├── core/           # Core functionality and business logic
│   ├── config.py           # Configuration management
│   └── semantic_search.py  # AI-powered search engine
├── gui/            # User interface components
│   ├── main_window.py      # Main application window
│   └── widgets.py          # Custom UI components
└── backend/        # System integration
    ├── clipboard_manager.py    # Backend interface
    ├── main.cpp               # C++ clipboard monitor
    └── CMakeLists.txt         # Build configuration
```

### Components:
1. **Backend Monitor**: C++ service for efficient system clipboard monitoring
2. **Core Engine**: Python-based semantic search and data management
3. **GUI Interface**: Modern PyQt6 application with rich user experience

## 🚀 Quick Start

### Automated Installation (Recommended)
```bash
git clone https://github.com/clipsage/clipsage.git
cd clipsage
chmod +x scripts/install.sh
./scripts/install.sh
```

### Manual Installation
```bash
# 1. Install system dependencies
sudo apt install python3 python3-pip cmake build-essential qt6-base-dev

# 2. Clone and setup
git clone https://github.com/clipsage/clipsage.git
cd clipsage
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Build backend
cd clipsage/backend && mkdir build && cd build
cmake .. && make -j$(nproc) && cp clipboard_manager ..

# 4. Install Ollama and model
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve & && ollama pull all-minilm:22m
```

### Package Installation
```bash
# Snap (coming soon)
sudo snap install clipsage

# Debian package (coming soon)  
wget https://github.com/clipsage/clipsage/releases/latest/download/clipsage_1.0.0_amd64.deb
sudo dpkg -i clipsage_1.0.0_amd64.deb
```

## 📖 Usage

### Starting ClipSage
```bash
# After installation
clipsage

# Or run directly
cd clipsage && source .venv/bin/activate
python -m clipsage

# With options
clipsage --help
clipsage --no-backend  # Run without starting clipboard monitor
clipsage --debug       # Enable debug output
```

### Using Semantic Search

1. **Basic Search:** Type any query in the search box and press Enter or click Search
2. **Semantic Queries:** Search by meaning, e.g.:
   - "programming code" - finds code snippets
   - "web links" - finds URLs
   - "meeting notes" - finds text about meetings
   - "configuration" - finds config-related content

3. **Clear Search:** Click "Clear" to show all clipboard items
4. **Refresh:** Click "Refresh" to update with new clipboard content

### Features in Detail

- **Auto-refresh:** The interface automatically refreshes every 5 seconds
- **Content Preview:** Click any item to see full content in the preview pane
- **Image Support:** Images are displayed with dimensions and path information
- **Type Detection:** Automatic classification of content types (text, image)

## File Structure

```
src/
├── app/                    # Python GUI application
│   ├── main.py            # Main PyQt6 application
│   ├── semantic.py        # Semantic search functionality
│   ├── clipsage.py        # Application launcher
│   ├── test_search.py     # Search functionality tests
│   ├── requirements.txt   # Python dependencies
│   └── pyproject.toml     # Project configuration
└── clip_board/            # C++ clipboard manager
    ├── main.cpp           # Clipboard monitoring service
    ├── CMakeLists.txt     # Build configuration
    ├── install.sh         # Build script
    └── run_clipboard_manager.sh  # Launcher script
```

## How It Works

### Data Flow
1. C++ service monitors system clipboard changes
2. Content is saved to `/tmp/clipboard_manager/` with timestamps
3. Python application loads and indexes this content
4. Semantic search uses Ollama embeddings for intelligent queries
5. Results are displayed in the modern GUI

### File Naming Convention
Clipboard files follow this pattern:
```
clip_{counter}_{timestamp}_{type}.{ext}
```
- `counter`: Sequential number
- `timestamp`: YYYY-MM-DD_HH-MM-SS-mmm format
- `type`: text, image (only these types are processed)
- `ext`: txt, png based on content type

## Troubleshooting

### Common Issues

1. **No clipboard items showing:**
   - Ensure the C++ clipboard manager is running
   - Check if `/tmp/clipboard_manager/` directory exists and has files
   - Copy some text to test clipboard monitoring

2. **Embedding errors:**
   - Verify Ollama is installed and running
   - Check that `all-minilm:22m` model is available: `ollama list`
   - Restart Ollama service if needed

3. **Search not working:**
   - Check Python dependencies are properly installed
   - Verify LangChain and Ollama packages are available
   - Check console output for error messages

### Debug Mode
Run with debug output:
```bash
cd src/app
python -c "from semantic import clipboard_search; clipboard_search.refresh_data()"
```

## Development

### Adding New Features
- The semantic search system is extensible
- UI components follow modern PyQt6 patterns
- The C++ component can be enhanced for additional MIME types

### Testing
```bash
cd src/app
python test_search.py
```

## Dependencies

### Python Packages
- PyQt6: Modern GUI framework
- LangChain: AI/ML framework for semantic search
- langchain-ollama: Ollama integration
- Pillow: Image processing
- docx: Document handling

### System Requirements
- Qt6 libraries
- C++ compiler (gcc/clang)
- CMake build system

## License

This project is open source. See the license file for details.

## Contributing

Contributions are welcome! Please submit pull requests with:
- Clear description of changes
- Updated documentation
- Test coverage for new features