import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout , QSizePolicy, QTextEdit
)
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from components.AddEntry.AddEntryWidget import createAddEntryWidget
from components.TablePreview import TablePreview
from utils.ApplyStyles import apply_styles

class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        self.table_preview = TablePreview(self)
        top_layout.addWidget(self.table_preview)

        self.add_entry_widget = createAddEntryWidget()
        
        self.add_entry_widget.add_button.clicked.connect(self.add_entry)
        top_layout.addWidget(self.add_entry_widget)

        self.add_entry_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addLayout(top_layout)

        self.testing = QTextEdit(self)
        self.testing.setPlaceholderText("Testing")
        main_layout.addWidget(self.testing)

        self.setLayout(main_layout)

        apply_styles(self)

    def add_entry(self):
        entry_data = self.add_entry_widget.collect_entry_data()
        self.table_preview.add_entry(entry_data)

    def save_entries(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.table_preview.entries, file)

    def load_entries(self, file_path):
        with open(file_path, 'r') as file:
            entries = json.load(file)
            self.table_preview.entries = entries
            self.table_preview.update_content()

    def set_content(self, content):
        self.table_preview.entries = content
        self.table_preview.update_content()

    def get_content(self):
        return self.table_preview.entries
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.add_entry()
