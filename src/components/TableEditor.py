from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from utils.Apply_Styles import apply_styles
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

        # Apply styles using the utility function
        apply_styles(self)

    def set_content(self, content):
        self.table_preview.setPlainText(content)
