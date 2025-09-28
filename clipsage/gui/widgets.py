"""
Custom GUI widgets for ClipSage
"""

from PyQt6.QtWidgets import (
    QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QGroupBox, QGridLayout, QCheckBox,
    QSpinBox, QComboBox, QSlider
)
from PyQt6.QtCore import Qt


class ModernButton(QPushButton):
    """Custom modern button with hover effects"""
    def __init__(self, text="", icon=None):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                font-size: 13px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border: 1px solid #21618c;
            }
            QPushButton:pressed {
                background-color: #21618c;
                padding-top: 9px;
                padding-bottom: 7px;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)


class SearchLineEdit(QLineEdit):
    """Modern search input with placeholder styling"""
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("🔍 Search clipboard items...")
        self.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #fefefe;
            }
            QLineEdit:hover {
                border-color: #bdc3c7;
            }
        """)


class ClipboardItemWidget(QWidget):
    """Custom widget for displaying clipboard items"""
    def __init__(self, text, item_type="text", timestamp=""):
        super().__init__()
        self.setup_ui(text, item_type, timestamp)
        
    def setup_ui(self, text, item_type, timestamp):
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        # Header with type and timestamp
        header_layout = QHBoxLayout()
        
        type_label = QLabel(f"📄 {item_type.title()}")
        type_style = "color: #7f8c8d; font-size: 12px; font-weight: 500;"
        type_label.setStyleSheet(type_style)
        
        time_label = QLabel(timestamp)
        time_label.setStyleSheet("color: #bdc3c7; font-size: 11px;")
        time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        header_layout.addWidget(type_label)
        header_layout.addStretch()
        header_layout.addWidget(time_label)
        
        # Content preview
        preview_text = text[:100] + "..." if len(text) > 100 else text
        content_label = QLabel(preview_text)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("""
            color: #2c3e50;
            font-size: 13px;
            line-height: 1.4;
            padding: 4px 0px;
        """)
        
        layout.addLayout(header_layout)
        layout.addWidget(content_label)
        self.setLayout(layout)


class ModernListWidget(QListWidget):
    """Enhanced list widget with modern styling"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #ecf0f1;
                border-radius: 8px;
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                outline: none;
            }
            QListWidget::item {
                border-bottom: 1px solid #ecf0f1;
                padding: 0px;
                margin: 0px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                border-left: 3px solid #3498db;
            }
            QListWidget::item:hover {
                background-color: #f5f5f5;
            }
        """)
        self.setAlternatingRowColors(True)


class ConfigurationPanel(QWidget):
    """Configuration panel widget"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # General Settings Group
        general_group = QGroupBox("General Settings")
        general_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 14px;
                color: #2c3e50;
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                background-color: white;
            }
        """)
        general_layout = QGridLayout()
        
        # Max items
        general_layout.addWidget(QLabel("Maximum items:"), 0, 0)
        max_items = QSpinBox()
        max_items.setRange(10, 10000)
        max_items.setValue(200)
        spinner_style = ("padding: 6px; border-radius: 4px; "
                         "border: 1px solid #bdc3c7;")
        max_items.setStyleSheet(spinner_style)
        general_layout.addWidget(max_items, 0, 1)
        
        # Auto-start
        auto_start = QCheckBox("Start with system")
        auto_start.setStyleSheet("font-size: 13px; padding: 4px;")
        general_layout.addWidget(auto_start, 1, 0, 1, 2)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Appearance Group
        appearance_group = QGroupBox("Appearance")
        appearance_group.setStyleSheet(general_group.styleSheet())
        appearance_layout = QGridLayout()
        
        appearance_layout.addWidget(QLabel("Theme:"), 0, 0)
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark", "Auto"])
        combo_style = ("padding: 6px; border-radius: 4px; "
                       "border: 1px solid #bdc3c7;")
        theme_combo.setStyleSheet(combo_style)
        appearance_layout.addWidget(theme_combo, 0, 1)
        
        appearance_layout.addWidget(QLabel("Font size:"), 1, 0)
        font_slider = QSlider(Qt.Orientation.Horizontal)
        font_slider.setRange(8, 18)
        font_slider.setValue(12)
        appearance_layout.addWidget(font_slider, 1, 1)
        
        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)
        
        layout.addStretch()
        self.setLayout(layout)