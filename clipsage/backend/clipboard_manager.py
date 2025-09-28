"""
Clipboard manager backend interface
"""

import subprocess
from pathlib import Path
from typing import Optional

from ..core.config import config


class ClipboardManager:
    """Interface for managing the C++ clipboard monitor"""
    
    def __init__(self, binary_path: Optional[Path] = None):
        self.binary_path = binary_path or self._find_binary()
        self.process: Optional[subprocess.Popen] = None
        
    def _find_binary(self) -> Path:
        """Find the clipboard manager binary"""
        # Check in the backend directory first
        backend_dir = Path(__file__).parent
        binary_path = backend_dir / "clipboard_manager"
        
        if binary_path.exists():
            return binary_path
            
        # Check in the original location
        project_root = Path(__file__).parent.parent.parent
        original_path = (project_root / "src" / "clip_board" /
                         "build" / "clipboard_manager")
        
        if original_path.exists():
            return original_path
            
        # Default path
        return Path("clipboard_manager")
    
    def is_running(self) -> bool:
        """Check if clipboard manager is running"""
        try:
            # Check our own process first
            if self.process and self.process.poll() is None:
                return True
                
            # Check system processes
            result = subprocess.run(
                ["pgrep", "-f", "clipboard_manager"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def start(self) -> bool:
        """Start the clipboard manager"""
        if self.is_running():
            print("Clipboard manager is already running")
            return True
            
        try:
            if not self.binary_path.exists():
                print(f"Clipboard manager binary not found: {self.binary_path}")
                return False
                
            # Start the process
            self.process = subprocess.Popen(
                [str(self.binary_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            print(f"Started clipboard manager (PID: {self.process.pid})")
            return True
            
        except Exception as e:
            print(f"Error starting clipboard manager: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop the clipboard manager"""
        try:
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                self.process = None
                
            # Also kill any other clipboard manager processes
            subprocess.run(["pkill", "-f", "clipboard_manager"], 
                          capture_output=True)
            
            print("Stopped clipboard manager")
            return True
            
        except Exception as e:
            print(f"Error stopping clipboard manager: {e}")
            return False
    
    def restart(self) -> bool:
        """Restart the clipboard manager"""
        self.stop()
        return self.start()
    
    def get_status(self) -> dict:
        """Get status information about the clipboard manager"""
        status = {
            "running": self.is_running(),
            "binary_path": str(self.binary_path),
            "binary_exists": self.binary_path.exists(),
            "clipboard_path": str(config.clipboard_path),
            "clipboard_path_exists": config.clipboard_path.exists()
        }
        
        if self.process:
            status["pid"] = self.process.pid
            status["managed_process"] = True
        else:
            status["managed_process"] = False
            
        return status


# Global instance
clipboard_manager = ClipboardManager()