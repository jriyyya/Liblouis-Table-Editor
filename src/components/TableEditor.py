from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from utils.ApplyStyles import apply_styles
from components.AddEntry.AddEntryWidget import createAddEntryWidget

class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        self.table_preview = QTextEdit(self)
        self.table_preview.setPlaceholderText("Table Preview")
        top_layout.addWidget(self.table_preview)

        self.add_entry_widget = createAddEntryWidget()
        top_layout.addWidget(self.add_entry_widget)

        self.add_entry_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addLayout(top_layout)

        self.testing = QTextEdit(self)
        self.testing.setPlaceholderText("Testing")
        main_layout.addWidget(self.testing)

        self.setLayout(main_layout)

        apply_styles(self)

    def set_content(self, content):
        self.table_preview.setPlainText(content)
