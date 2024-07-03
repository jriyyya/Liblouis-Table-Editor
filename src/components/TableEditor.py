# table_editor.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel

class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
        
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Horizontal layout for the top two components
        top_layout = QHBoxLayout()

        # Table preview component (left)
        self.table_preview = QTextEdit(self)
        self.table_preview.setPlaceholderText("Table Preview")
        top_layout.addWidget(self.table_preview)

        # Add entry component (right)
        self.add_entry = QTextEdit(self)
        self.add_entry.setPlaceholderText("Add Entry")
        top_layout.addWidget(self.add_entry)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(top_layout)

        # Testing component (bottom)
        self.testing = QTextEdit(self)
        self.testing.setPlaceholderText("Testing")
        main_layout.addWidget(self.testing)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def set_content(self, content):
        self.table_preview.setPlainText(content)
