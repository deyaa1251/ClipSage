"""
Main window for ClipSage application
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem,
    QTextEdit, QSplitter, QTabWidget, QLabel, QFrame, QHeaderView,
    QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

# Use optimized version for better performance
try:
    from ..core.semantic_search_optimized import (
        OptimizedClipboardSemanticSearch as ClipboardSemanticSearch
    )
except ImportError:
    from ..core.semantic_search import ClipboardSemanticSearch
from ..core.config import config
from .widgets import (
    ModernButton, SearchLineEdit, ClipboardItemWidget,
    ModernListWidget, ConfigurationPanel
)


class ClipboardManagerUI(QMainWindow):
    """Main clipboard manager window"""
    
    def __init__(self):
        super().__init__()
        self.clipboard_search = ClipboardSemanticSearch()
        self.clipboard_items = []
        self.current_search_results = []
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        self.load_clipboard_data()
        
        # Setup auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_clipboard_data)
        self.refresh_timer.start(config.refresh_interval)
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("ClipSage - Advanced Clipboard Manager")
        
        # Load window geometry from config
        self.setGeometry(
            config.get("window.x", 100),
            config.get("window.y", 100),
            config.get("window.width", 1200),
            config.get("window.height", 800)
        )
        
        # Apply modern styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #ecf0f1;
                border-radius: 8px;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #ffffff;
                color: #2c3e50;
                border: 1px solid #ecf0f1;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
                border-bottom: none;
            }
            QTabBar::tab:hover:!selected {
                background-color: #ecf0f1;
            }
        """)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Main clipboard tab
        self.setup_main_tab()
        
        # Configuration tab
        self.setup_config_tab()
        
        # Statistics tab
        self.setup_stats_tab()
        
        main_layout.addWidget(self.tab_widget)
        central_widget.setLayout(main_layout)
        
    def setup_main_tab(self):
        """Setup the main clipboard management tab"""
        main_tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = SearchLineEdit()
        search_button = ModernButton("Search")
        clear_button = ModernButton("Clear")
        refresh_button = ModernButton("Refresh")
        
        # Style the clear button as red
        red_style = (clear_button.styleSheet()
                     .replace("#3498db", "#e74c3c")
                     .replace("#2980b9", "#c0392b")
                     .replace("#21618c", "#a93226"))
        clear_button.setStyleSheet(red_style)
        
        # Connect search functionality
        search_button.clicked.connect(self.perform_search)
        clear_button.clicked.connect(self.clear_search)
        refresh_button.clicked.connect(self.refresh_clipboard_data)
        self.search_input.returnPressed.connect(self.perform_search)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(clear_button)
        search_layout.addWidget(refresh_button)
        layout.addLayout(search_layout)
        
        # Main content splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Clipboard items
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Items list
        self.items_list = ModernListWidget()
        self.items_list.setMinimumWidth(400)
        self.items_list.itemClicked.connect(self.on_item_selected)
        
        # Control buttons
        buttons_layout = QHBoxLayout()
        pin_button = ModernButton("📌 Pin")
        edit_button = ModernButton("✏️ Edit")
        delete_button = ModernButton("🗑️ Delete")
        
        delete_red_style = (delete_button.styleSheet()
                            .replace("#3498db", "#e74c3c")
                            .replace("#2980b9", "#c0392b")
                            .replace("#21618c", "#a93226"))
        delete_button.setStyleSheet(delete_red_style)
        
        buttons_layout.addWidget(pin_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()
        
        left_layout.addWidget(QLabel("Clipboard Items"))
        left_layout.addWidget(self.items_list)
        left_layout.addLayout(buttons_layout)
        left_panel.setLayout(left_layout)
        
        # Right panel - Preview and details
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Preview area
        right_layout.addWidget(QLabel("Preview"))
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ecf0f1;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                line-height: 1.4;
            }
        """)
        right_layout.addWidget(self.preview_text)
        
        # Item details
        details_frame = QFrame()
        details_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        details_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #ecf0f1;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 10px;
            }
        """)
        
        details_layout = QVBoxLayout()
        details_layout.addWidget(QLabel("Item Details"))
        details_frame.setLayout(details_layout)
        right_layout.addWidget(details_frame)
        
        right_panel.setLayout(right_layout)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
        main_tab.setLayout(layout)
        self.tab_widget.addTab(main_tab, "📋 Clipboard")
        
    def setup_config_tab(self):
        """Setup configuration tab"""
        config_tab = ConfigurationPanel()
        self.tab_widget.addTab(config_tab, "⚙️ Settings")
        
    def setup_stats_tab(self):
        """Setup statistics tab"""
        stats_tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Clipboard Statistics"))
        
        # Statistics table
        stats_table = QTableWidget(0, 2)
        stats_table.setHorizontalHeaderLabels(["Metric", "Value"])
        header = stats_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1,
                                   QHeaderView.ResizeMode.ResizeToContents)
        
        # Add some sample statistics
        self.update_statistics_table(stats_table)
        
        layout.addWidget(stats_table)
        stats_tab.setLayout(layout)
        self.tab_widget.addTab(stats_tab, "📊 Statistics")
        
    def setup_menu_bar(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #ffffff;
                color: #2c3e50;
                border-bottom: 1px solid #ecf0f1;
                font-size: 13px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu('File')
        file_menu.addAction('New Item')
        file_menu.addAction('Import...')
        file_menu.addAction('Export...')
        file_menu.addSeparator()
        file_menu.addAction('Exit')
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction('Copy')
        edit_menu.addAction('Paste')
        edit_menu.addAction('Delete')
        edit_menu.addSeparator()
        edit_menu.addAction('Select All')
        
        # View menu
        view_menu = menubar.addMenu('View')
        view_menu.addAction('Refresh')
        view_menu.addAction('Toggle Preview')
        view_menu.addSeparator()
        view_menu.addAction('Full Screen')
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        help_menu.addAction('About')
        help_menu.addAction('Documentation')
        
    def setup_toolbar(self):
        """Setup toolbar"""
        toolbar = self.addToolBar('Main')
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #ffffff;
                border: none;
                border-bottom: 1px solid #ecf0f1;
                spacing: 4px;
                padding: 4px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 6px;
                margin: 2px;
            }
            QToolButton:hover {
                background-color: #ecf0f1;
                border-color: #bdc3c7;
            }
            QToolButton:pressed {
                background-color: #d5dbdb;
            }
        """)
        
        # Add toolbar actions
        toolbar.addAction('📋 New')
        toolbar.addAction('📁 Import')
        toolbar.addAction('💾 Export')
        toolbar.addSeparator()
        toolbar.addAction('🔍 Search')
        toolbar.addAction('⚙️ Settings')
        toolbar.addSeparator()
        toolbar.addAction('❓ Help')
        
    def setup_status_bar(self):
        """Setup status bar"""
        status = self.statusBar()
        status.setStyleSheet("""
            QStatusBar {
                background-color: #ffffff;
                color: #7f8c8d;
                border-top: 1px solid #ecf0f1;
                padding: 4px;
            }
        """)
        status.showMessage("Ready")
        
    def update_statistics_table(self, table):
        """Update statistics table with current data"""
        stats = [
            ("Total Items", len(self.clipboard_items)),
            ("Text Items", len([i for i in self.clipboard_items
                               if i.get('type') == 'text'])),
            ("Image Items", len([i for i in self.clipboard_items
                                if i.get('type') == 'image'])),
            ("Search Results", len(self.current_search_results)),
        ]
        
        table.setRowCount(len(stats))
        for i, (metric, value) in enumerate(stats):
            table.setItem(i, 0, QTableWidgetItem(metric))
            table.setItem(i, 1, QTableWidgetItem(str(value)))
    
    def load_clipboard_data(self):
        """Load clipboard items from the semantic search system"""
        try:
            self.clipboard_search.refresh_data()
            self.clipboard_items = self.clipboard_search.get_all_items()
            self.update_items_display(self.clipboard_items)
            self.update_status_bar()
        except Exception as e:
            print(f"Error loading clipboard data: {e}")
            self.clipboard_items = []
    
    def refresh_clipboard_data(self):
        """Refresh clipboard data and update display"""
        # Only refresh if window is visible to save resources
        if self.isVisible():
            self.load_clipboard_data()
    
    def update_items_display(self, items):
        """Update the items list widget with given items"""
        self.items_list.clear()
        
        for item_data in items:
            list_item = QListWidgetItem()
            
            # Extract display information
            preview = item_data.get("preview", "")
            item_type = item_data.get("type", "text")
            timestamp = item_data.get("timestamp", "Unknown")
            
            # Create custom widget
            widget = ClipboardItemWidget(preview, item_type, timestamp)
            list_item.setSizeHint(widget.sizeHint())
            
            # Store the full item data
            list_item.setData(Qt.ItemDataRole.UserRole, item_data)
            
            self.items_list.addItem(list_item)
            self.items_list.setItemWidget(list_item, widget)
    
    def perform_search(self):
        """Perform semantic search on clipboard items"""
        query = self.search_input.text().strip()
        if not query:
            self.clear_search()
            return
        
        try:
            max_results = config.get("search.max_results", 10)
            search_results = self.clipboard_search.search(query, k=max_results)
            self.current_search_results = search_results
            self.update_items_display(search_results)
            self.update_status_bar(f"Found {len(search_results)} results")
        except Exception as e:
            print(f"Error performing search: {e}")
            self.update_status_bar("Search error")
    
    def clear_search(self):
        """Clear search and show all items"""
        self.search_input.clear()
        self.current_search_results = []
        self.update_items_display(self.clipboard_items)
        self.update_status_bar()
    
    def on_item_selected(self, item):
        """Handle item selection"""
        item_data = item.data(Qt.ItemDataRole.UserRole)
        if item_data:
            content = item_data.get("content", "")
            self.preview_text.setPlainText(content)
            
            # Update details if needed
            metadata = item_data.get("metadata", {})
            files = metadata.get("files", {})
            
            # Handle image display if it's an image item
            if item_data.get("type") == "image" and "image" in files:
                try:
                    image_path = files["image"]
                    pixmap = QPixmap(str(image_path))
                    if not pixmap.isNull():
                        # Show image info in text preview
                        info = (f"Image: {image_path}\n"
                                f"Size: {pixmap.width()}x{pixmap.height()}\n\n"
                                f"{content}")
                        self.preview_text.setPlainText(info)
                except Exception as e:
                    print(f"Error loading image: {e}")
    
    def update_status_bar(self, message=None):
        """Update status bar with item count or custom message"""
        if message:
            self.statusBar().showMessage(message)
        else:
            count = len(self.clipboard_items)
            self.statusBar().showMessage(f"Ready - {count} items in clipboard")
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save window geometry to config
        geometry = self.geometry()
        config.set("window.x", geometry.x())
        config.set("window.y", geometry.y())
        config.set("window.width", geometry.width())
        config.set("window.height", geometry.height())
        config.save_config()
        
        # Cleanup resources
        if hasattr(self.clipboard_search, 'cleanup'):
            self.clipboard_search.cleanup()
        
        event.accept()
