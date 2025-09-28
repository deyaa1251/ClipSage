"""
Semantic search functionality for clipboard manager
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from PIL import Image

from .config import config


class ClipboardSemanticSearch:
    """Semantic search functionality for clipboard manager"""
    
    def __init__(self, model_name: Optional[str] = None,
                 clipboard_path: Optional[Path] = None):
        self.model_name = model_name or config.embedding_model
        self.embed = OllamaEmbeddings(model=self.model_name)
        self.vector_store = InMemoryVectorStore(self.embed)
        self.clipboard_path = clipboard_path or config.clipboard_path
        self.documents = []
        self.file_mapping = {}  # Maps document ids to file paths
        
        # Ensure clipboard directory exists
        if not self.clipboard_path.exists():
            self.clipboard_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing clipboard data
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh clipboard data from the filesystem"""
        if not self.clipboard_path.exists():
            return
        
        self.documents = []
        self.file_mapping = {}
        text_documents = []
        
        # Get all clipboard files
        clipboard_files = list(self.clipboard_path.glob("*"))
        
        # Group files by clipboard entry
        entries = {}
        for file_path in clipboard_files:
            filename = file_path.name
            # Extract counter and timestamp from filename
            if filename.startswith("clip_"):
                parts = filename.split("_")
                if len(parts) >= 3:
                    counter = parts[1]
                    # Get date and time parts
                    timestamp = "_".join(parts[2:]).split("_")[0:3]
                    timestamp_str = "_".join(timestamp)
                    
                    entry_key = f"{counter}_{timestamp_str}"
                    if entry_key not in entries:
                        entries[entry_key] = {}
                    
                    # Only process text and image files
                    if filename.endswith("_text.txt"):
                        entries[entry_key]["text"] = file_path
                    elif filename.endswith("_image.png"):
                        entries[entry_key]["image"] = file_path
                    # Skip HTML, URLs, and formats files
        
        # Process each clipboard entry
        for entry_key, files in entries.items():
            doc_id = f"clip_{entry_key}"
            content = ""
            metadata = {
                "entry_id": entry_key,
                "files": files,
                "timestamp": self._extract_timestamp(entry_key),
                "type": "mixed"
            }
            
            # Process text content
            if "text" in files:
                try:
                    text_file = files["text"]
                    with open(text_file, "r", encoding="utf-8",
                              errors="ignore") as f:
                        text_content = f.read().strip()
                        if text_content:
                            content += f"Text: {text_content}\n"
                            metadata["type"] = "text"
                            metadata["preview"] = text_content[:100]
                except Exception as e:
                    print(f"Error reading text file {files['text']}: {e}")
            
            # Handle image content
            if "image" in files:
                try:
                    # For images, we'll add a description
                    image_path = files["image"]
                    with Image.open(image_path) as img:
                        width, height = img.size
                        img_desc = f"Image: {width}x{height} pixels"
                        content += f"{img_desc} from {image_path.name}\n"
                        # If we have no text content, make this an image type
                        if (not metadata.get("type") or
                                metadata["type"] == "mixed"):
                            metadata["type"] = "image"
                            metadata["preview"] = f"Image ({width}x{height})"
                        metadata["image_path"] = str(image_path)
                except Exception as e:
                    print(f"Error processing image file {files['image']}: {e}")
            
            # Only add if we have content
            if content.strip():
                doc = Document(
                    page_content=content.strip(),
                    metadata=metadata
                )
                self.documents.append(doc)
                self.file_mapping[doc_id] = files
                text_documents.append(doc)
        
        # Add documents to vector store if we have any
        if text_documents:
            try:
                self.vector_store.add_documents(documents=text_documents)
                count = len(text_documents)
                print(f"Loaded {count} clipboard entries for semantic search")
            except Exception as e:
                print(f"Error adding documents to vector store: {e}")
    
    def _extract_timestamp(self, entry_key: str) -> str:
        """Extract readable timestamp from entry key"""
        try:
            # entry_key format: counter_date_time
            parts = entry_key.split("_")
            if len(parts) >= 3:
                date_part = parts[1]  # yyyy-MM-dd
                time_part = parts[2]  # hh-mm-ss
                
                # Convert to readable format
                date_readable = date_part.replace("-", "/")
                time_readable = time_part.replace("-", ":")
                
                return f"{date_readable} {time_readable}"
        except Exception:
            pass
        return entry_key
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search on clipboard data"""
        if not query.strip():
            return []
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            
            search_results = []
            for doc in results:
                preview = doc.metadata.get("preview", doc.page_content[:100])
                result = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "preview": preview,
                    "type": doc.metadata.get("type", "text"),
                    "timestamp": doc.metadata.get("timestamp", "Unknown"),
                    "files": doc.metadata.get("files", {})
                }
                search_results.append(result)
            
            return search_results
        except Exception as e:
            print(f"Error performing semantic search: {e}")
            return []
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """Get all clipboard items"""
        items = []
        for doc in self.documents:
            preview = doc.metadata.get("preview", doc.page_content[:100])
            item = {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "preview": preview,
                "type": doc.metadata.get("type", "text"),
                "timestamp": doc.metadata.get("timestamp", "Unknown"),
                "files": doc.metadata.get("files", {})
            }
            items.append(item)
        
        # Sort by timestamp (newest first)
        items.sort(key=lambda x: x["timestamp"], reverse=True)
        return items
    
    def get_item_content(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Get full content of a specific clipboard item"""
        for doc in self.documents:
            if doc.metadata.get("entry_id") == entry_id:
                return {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "files": doc.metadata.get("files", {})
                }
        return None


# Global instance for backward compatibility
clipboard_search = ClipboardSemanticSearch()


def search_clipboard(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Convenience function for searching clipboard"""
    return clipboard_search.search(query, k)


def refresh_clipboard_data():
    """Convenience function to refresh clipboard data"""
    clipboard_search.refresh_data()


def get_all_clipboard_items() -> List[Dict[str, Any]]:
    """Convenience function to get all clipboard items"""
    return clipboard_search.get_all_items()