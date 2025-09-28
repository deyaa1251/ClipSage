"""
Core functionality for ClipSage
"""

from .config import Config, config
from .semantic_search import ClipboardSemanticSearch

__all__ = ["Config", "config", "ClipboardSemanticSearch"]