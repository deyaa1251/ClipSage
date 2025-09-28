#!/usr/bin/env python3
"""
Performance test script for ClipSage
"""

import sys
import time
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from clipsage.core.semantic_search_optimized import OptimizedClipboardSemanticSearch
from clipsage.core.semantic_search import ClipboardSemanticSearch
from clipsage.core.performance import performance_monitor


def create_test_data(clipboard_path: Path, num_entries: int = 100) -> None:
    """Create test clipboard data"""
    print(f"Creating {num_entries} test clipboard entries...")
    
    clipboard_path.mkdir(parents=True, exist_ok=True)
    
    for i in range(num_entries):
        # Create text files
        text_content = f"Test clipboard entry {i} with some sample content for semantic search testing. This is entry number {i} of {num_entries}."
        text_file = clipboard_path / f"clip_{i:03d}_2024-01-{(i%30)+1:02d}_10-{(i%60):02d}-00_text.txt"
        
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        # Create some image placeholders (every 5th entry)
        if i % 5 == 0:
            from PIL import Image
            import io
            
            # Create a small test image
            img = Image.new('RGB', (100, 100), color='red')
            img_file = clipboard_path / f"clip_{i:03d}_2024-01-{(i%30)+1:02d}_10-{(i%60):02d}-00_image.png"
            img.save(img_file)


def benchmark_search_system(search_class, test_data_path: Path, num_queries: int = 50) -> Dict[str, float]:
    """Benchmark the search system performance"""
    print(f"Benchmarking {search_class.__name__}...")
    
    # Initialize search system
    start_time = time.time()
    search_system = search_class(clipboard_path=test_data_path)
    init_time = time.time() - start_time
    
    # Test refresh performance
    start_time = time.time()
    search_system.refresh_data(force=True)
    refresh_time = time.time() - start_time
    
    # Test search performance
    test_queries = [
        "test clipboard entry",
        "sample content",
        "semantic search",
        "entry number",
        "testing data",
        "clipboard manager",
        "performance test",
        "sample text content"
    ]
    
    search_times = []
    for i in range(num_queries):
        query = test_queries[i % len(test_queries)] + f" {i}"
        
        start_time = time.time()
        results = search_system.search(query, k=5)
        search_time = time.time() - start_time
        search_times.append(search_time)
    
    # Test get_all_items performance
    start_time = time.time()
    all_items = search_system.get_all_items()
    get_all_time = time.time() - start_time
    
    # Cleanup
    if hasattr(search_system, 'cleanup'):
        search_system.cleanup()
    
    return {
        "init_time": init_time,
        "refresh_time": refresh_time,
        "avg_search_time": sum(search_times) / len(search_times),
        "max_search_time": max(search_times),
        "min_search_time": min(search_times),
        "get_all_time": get_all_time,
        "total_items": len(all_items)
    }


def compare_implementations(test_sizes: List[int] = [50, 100, 200, 500]):
    """Compare original vs optimized implementations"""
    print("=== ClipSage Performance Comparison ===\n")
    
    results = {}
    
    for size in test_sizes:
        print(f"\n--- Testing with {size} clipboard entries ---")
        
        # Create temporary test data
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "clipboard_test"
            create_test_data(test_path, size)
            
            # Test original implementation
            try:
                original_results = benchmark_search_system(ClipboardSemanticSearch, test_path)
                print(f"Original Implementation:")
                print(f"  Init time: {original_results['init_time']:.3f}s")
                print(f"  Refresh time: {original_results['refresh_time']:.3f}s")
                print(f"  Avg search time: {original_results['avg_search_time']*1000:.1f}ms")
                print(f"  Get all items: {original_results['get_all_time']*1000:.1f}ms")
            except Exception as e:
                print(f"Original implementation failed: {e}")
                original_results = None
            
            # Test optimized implementation
            try:
                optimized_results = benchmark_search_system(OptimizedClipboardSemanticSearch, test_path)
                print(f"Optimized Implementation:")
                print(f"  Init time: {optimized_results['init_time']:.3f}s")
                print(f"  Refresh time: {optimized_results['refresh_time']:.3f}s")
                print(f"  Avg search time: {optimized_results['avg_search_time']*1000:.1f}ms")
                print(f"  Get all items: {optimized_results['get_all_time']*1000:.1f}ms")
                
                # Calculate improvements
                if original_results:
                    refresh_improvement = ((original_results['refresh_time'] - optimized_results['refresh_time']) / original_results['refresh_time']) * 100
                    search_improvement = ((original_results['avg_search_time'] - optimized_results['avg_search_time']) / original_results['avg_search_time']) * 100
                    
                    print(f"Improvements:")
                    print(f"  Refresh time: {refresh_improvement:+.1f}%")
                    print(f"  Search time: {search_improvement:+.1f}%")
            except Exception as e:
                print(f"Optimized implementation failed: {e}")
                optimized_results = None
            
            results[size] = {
                "original": original_results,
                "optimized": optimized_results
            }
    
    return results


def memory_usage_test(duration_minutes: int = 2):
    """Test memory usage over time"""
    print(f"\n--- Memory Usage Test ({duration_minutes} minutes) ---")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir) / "clipboard_test"
        create_test_data(test_path, 200)
        
        search_system = OptimizedClipboardSemanticSearch(clipboard_path=test_path)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        memory_samples = []
        
        print("Monitoring memory usage...")
        while time.time() < end_time:
            # Trigger refresh and search operations
            search_system.refresh_data()
            
            # Perform some searches
            for query in ["test", "content", "clipboard", "entry"]:
                search_system.search(query, k=5)
            
            # Update performance monitor
            performance_monitor.update_system_metrics()
            
            current_metrics = performance_monitor.get_current_metrics()
            if current_metrics:
                memory_samples.append(current_metrics.memory_mb)
                print(f"Memory: {current_metrics.memory_mb:.1f}MB, CPU: {current_metrics.cpu_percent:.1f}%")
            
            time.sleep(10)  # Sample every 10 seconds
        
        search_system.cleanup()
        
        if memory_samples:
            print(f"\nMemory Usage Summary:")
            print(f"  Average: {sum(memory_samples)/len(memory_samples):.1f}MB")
            print(f"  Peak: {max(memory_samples):.1f}MB")
            print(f"  Samples: {len(memory_samples)}")


def main():
    """Run performance tests"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "memory":
            memory_usage_test(int(sys.argv[2]) if len(sys.argv) > 2 else 2)
            return
        elif sys.argv[1] == "quick":
            compare_implementations([50, 100])
            return
    
    # Full performance test
    results = compare_implementations()
    
    print("\n=== Performance Summary ===")
    for size, data in results.items():
        if data["original"] and data["optimized"]:
            orig = data["original"]
            opt = data["optimized"]
            
            refresh_improvement = ((orig['refresh_time'] - opt['refresh_time']) / orig['refresh_time']) * 100
            search_improvement = ((orig['avg_search_time'] - opt['avg_search_time']) / orig['avg_search_time']) * 100
            
            print(f"{size} entries: Refresh {refresh_improvement:+.1f}%, Search {search_improvement:+.1f}%")
    
    # Run a quick memory test
    memory_usage_test(1)


if __name__ == "__main__":
    main()