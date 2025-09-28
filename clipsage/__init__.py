"""
ClipSage - Advanced Clipboard Manager with Semantic Search

A modern clipboard manager that combines intelligent semantic search with 
a clean PyQt6 interface and efficient C++ backend monitoring.
"""

__version__ = "1.0.0"
__author__ = "ClipSage Team"
__email__ = "contact@clipsage.org"
__description__ = "Advanced Clipboard Manager with Semantic Search"

# Public API exports
from .core.semantic_search import ClipboardSemanticSearch
from .core.config import Config

__all__ = [
    "ClipboardSemanticSearch",
    "Config",
    "__version__",
]