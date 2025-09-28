# ClipSage Project Structure

This document provides an overview of the ClipSage project structure and organization.

## 📁 Directory Structure

```
ClipSage/
├── 📦 clipsage/                   # Main Python package
│   ├── __init__.py               # Package initialization and public API
│   ├── 🧠 core/                  # Core functionality
│   │   ├── __init__.py           # Core module exports
│   │   ├── config.py             # Configuration management
│   │   └── semantic_search.py   # AI-powered search engine
│   ├── 🎨 gui/                   # User interface components
│   │   ├── __init__.py           # GUI module exports
│   │   ├── main_window.py        # Main application window
│   │   └── widgets.py            # Custom UI widgets
│   └── ⚙️ backend/               # System integration
│       ├── __init__.py           # Backend module exports
│       ├── clipboard_manager.py  # Python interface to C++ backend
│       ├── main.cpp              # C++ clipboard monitor
│       └── CMakeLists.txt        # C++ build configuration
├── 🔧 scripts/                   # Installation and utility scripts
│   └── install.sh               # Automated installation script
├── 📦 packaging/                 # Package configurations
│   ├── snap/                    # Snap package
│   │   └── snapcraft.yaml      # Snap configuration
│   ├── deb/                     # Debian package
│   │   └── DEBIAN/              # Debian package metadata
│   └── appimage/                # AppImage configuration
├── 🧪 tests/                     # Test suite
│   ├── __init__.py              # Test package initialization
│   └── test_semantic_search.py  # Semantic search tests
├── 📚 docs/                      # Documentation
│   └── INSTALL.md               # Installation guide
├── __main__.py                  # Application entry point
├── pyproject.toml               # Project configuration
├── requirements.txt             # Python dependencies
└── README.md                    # Project overview
```

## 🏗️ Architecture Overview

### Core Components

#### 1. **Core Module** (`clipsage/core/`)
- **Purpose**: Business logic and data management
- **Components**:
  - `config.py`: Centralized configuration management with JSON storage
  - `semantic_search.py`: AI-powered search engine using Ollama embeddings

#### 2. **GUI Module** (`clipsage/gui/`)
- **Purpose**: User interface and user experience
- **Components**:
  - `main_window.py`: Main application window with tabs and functionality
  - `widgets.py`: Reusable custom UI components (buttons, lists, panels)

#### 3. **Backend Module** (`clipsage/backend/`)
- **Purpose**: System-level clipboard monitoring
- **Components**:
  - `clipboard_manager.py`: Python interface for managing the C++ backend
  - `main.cpp`: Efficient C++ clipboard monitor with Qt6
  - `CMakeLists.txt`: Build system for the C++ component

### Data Flow

```
System Clipboard → C++ Monitor → File System → Python Core → GUI
                   (main.cpp)     (/tmp/...)   (semantic.py)  (main_window.py)
```

1. **Capture**: C++ monitor detects clipboard changes
2. **Storage**: Content saved to organized file structure
3. **Indexing**: Python core loads and indexes content for search
4. **Search**: AI-powered semantic search through indexed content
5. **Display**: GUI presents results with preview and interaction

## 🎯 Design Principles

### Modularity
- Clear separation between GUI, core logic, and system integration
- Each module has well-defined responsibilities and interfaces
- Easy to test, maintain, and extend individual components

### Configuration-Driven
- Centralized configuration management
- User preferences stored in `~/.config/clipsage/`
- Runtime behavior configurable without code changes

### Cross-Platform Ready
- Abstract interfaces for system-specific functionality
- Qt6 provides cross-platform GUI framework
- CMake for portable C++ builds

### Performance Optimized
- C++ backend for efficient system monitoring
- Lazy loading of clipboard content
- Efficient vector storage for semantic search

## 📋 File Naming Conventions

### Clipboard Files
```
/tmp/clipboard_manager/clip_{counter}_{timestamp}_{type}.{ext}
```
- `counter`: Sequential number (6 digits, zero-padded)
- `timestamp`: YYYY-MM-DD_HH-MM-SS-mmm format
- `type`: content type (text, image)
- `ext`: file extension (txt, png)

### Python Modules
- Snake_case for file names and functions
- PascalCase for class names
- Descriptive names indicating purpose

### Configuration
- JSON format for human readability
- Hierarchical structure for organization
- Default values with user overrides

## 🔧 Build System

### Python Package
- Uses modern `pyproject.toml` configuration
- Setuptools backend for compatibility
- Includes C++ sources as package data

### C++ Backend
- CMake for cross-platform builds
- Qt6 for clipboard and GUI functionality
- Release builds optimized for performance

### Packaging
- Multiple distribution formats supported
- Snap for universal Linux distribution
- Debian packages for apt-based systems
- AppImage for portable execution

## 🧪 Testing Strategy

### Unit Tests
- Core functionality tested in isolation
- Mock external dependencies (filesystem, Qt)
- Semantic search accuracy validation

### Integration Tests
- End-to-end workflow testing
- GUI interaction simulation
- Backend communication verification

### Package Tests
- Installation verification
- Desktop integration testing
- Cross-distribution compatibility

## 📈 Extensibility

### Adding New Content Types
1. Extend C++ monitor to capture new MIME types
2. Add processing logic in `semantic_search.py`
3. Update GUI widgets to display new types

### Adding New Search Algorithms
1. Implement in `core/semantic_search.py`
2. Add configuration options in `core/config.py`
3. Expose settings in GUI configuration panel

### Adding New Platforms
1. Create platform-specific backend implementation
2. Add build configuration for new platform
3. Update packaging scripts for distribution

This modular architecture ensures ClipSage remains maintainable and extensible while providing a robust foundation for advanced clipboard management.