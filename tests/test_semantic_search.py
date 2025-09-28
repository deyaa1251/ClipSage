"""
Test the semantic search functionality
"""

import unittest
import tempfile
from pathlib import Path

from clipsage.core.semantic_search import ClipboardSemanticSearch


class TestSemanticSearch(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.clipboard_path = self.temp_dir / "clipboard_manager"
        self.clipboard_path.mkdir(parents=True)
        
        # Create some test clipboard files
        self.create_test_files()
        
        # Initialize semantic search with test directory
        self.search = ClipboardSemanticSearch(
            clipboard_path=self.clipboard_path
        )
    
    def create_test_files(self):
        """Create test clipboard files"""
        # Text file 1
        text_file1 = self.clipboard_path / "clip_000001_2025-09-28_10-30-45_text.txt"
        text_file1.write_text("Hello world, this is a test document about programming")
        
        # Text file 2
        text_file2 = self.clipboard_path / "clip_000002_2025-09-28_10-31-00_text.txt"
        text_file2.write_text("System configuration and settings for the application")
        
        # Create corresponding format files
        format_file1 = self.clipboard_path / "clip_000001_2025-09-28_10-30-45_formats.txt"
        format_file1.write_text("Available formats:\n  - text/plain")
        
        format_file2 = self.clipboard_path / "clip_000002_2025-09-28_10-31-00_formats.txt"
        format_file2.write_text("Available formats:\n  - text/plain")
    
    def test_load_items(self):
        """Test loading clipboard items"""
        items = self.search.get_all_items()
        self.assertEqual(len(items), 2)
        
        # Check that both items were loaded
        contents = [item['content'] for item in items]
        self.assertTrue(any("Hello world" in content for content in contents))
        self.assertTrue(any("System configuration" in content for content in contents))
    
    def test_search_functionality(self):
        """Test semantic search"""
        # Search for programming-related content
        results = self.search.search("programming", k=5)
        self.assertGreater(len(results), 0)
        
        # Search for system-related content
        results = self.search.search("system", k=5)
        self.assertGreater(len(results), 0)
    
    def test_item_types(self):
        """Test that items have correct types"""
        items = self.search.get_all_items()
        for item in items:
            self.assertIn('type', item)
            self.assertIn('preview', item)
            self.assertIn('timestamp', item)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == '__main__':
    unittest.main()