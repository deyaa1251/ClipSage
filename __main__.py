"""
ClipSage main application entry point
"""

import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from clipsage.core.config import config
from clipsage.gui.main_window import ClipboardManagerUI
from clipsage.backend.clipboard_manager import clipboard_manager


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="ClipSage - Advanced Clipboard Manager with Semantic Search"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--no-backend",
        action="store_true",
        help="Don't start the clipboard manager backend"
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug output"
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="ClipSage 1.0.0"
    )
    
    return parser.parse_args()


def ensure_backend_running():
    """Ensure the clipboard manager backend is running"""
    if not clipboard_manager.is_running():
        print("Starting clipboard manager backend...")
        if not clipboard_manager.start():
            print("Warning: Failed to start clipboard manager backend")
            print("You may need to start it manually")
        else:
            print("Clipboard manager backend started successfully")
    else:
        print("Clipboard manager backend is already running")


def main():
    """Main application entry point"""
    args = parse_arguments()
    
    # Load custom config if specified
    if args.config:
        from clipsage.core.config import Config
        global config
        config = Config(args.config)
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("ClipSage")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("ClipSage")
    app.setOrganizationDomain("clipsage.org")
    
    # Start backend if requested
    if not args.no_backend:
        ensure_backend_running()
    
    # Create and show main window
    try:
        window = ClipboardManagerUI()
        window.show()
        
        # Run the application
        sys.exit(app.exec())
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()