from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from components.AddEntryWidget import createAddEntryWidget

class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        # Main vertical layout
        main_layout = QVBoxLayout()

        # Horizontal layout for the top two components
        top_layout = QHBoxLayout()

        # Table preview component (left)
        self.table_preview = QTextEdit(self)
        self.table_preview.setPlaceholderText("Table Preview")
        top_layout.addWidget(self.table_preview)

        # Add entry widget (right)
        self.add_entry_widget = createAddEntryWidget()
        top_layout.addWidget(self.add_entry_widget)

        # Set size policy for AddEntryWidget
        self.add_entry_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(top_layout)

        # Testing component (bottom)
        self.testing = QTextEdit(self)
        self.testing.setPlaceholderText("Testing")
        main_layout.addWidget(self.testing)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        self.apply_styles()

    def set_content(self, content):
        self.table_preview.setPlainText(content)

    def apply_styles(self):
        self.setStyleSheet("""
            QTextEdit {
                background: #FFFFFF;
                padding: 10px;
                font-family: Verdana, sans-serif;
                font-size: 16px;  /* Larger font size */
                color: black;  /* Text color */
            }
            QTextEdit::placeholder {
                color: #888888;
            }
        """)

        # Apply styles to individual text edits
        self.table_preview.setStyleSheet("QTextEdit { background: #FFFFFF; }")
        self.add_entry_widget.setStyleSheet("QTextEdit { background: #FFFFFF; }")
        self.testing.setStyleSheet("QTextEdit { background: #FFFFFF; }")
