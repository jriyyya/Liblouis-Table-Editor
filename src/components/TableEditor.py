import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog
)
from components.AddEntry.AddEntryWidget import createAddEntryWidget
from components.TablePreview import TablePreview

class TableEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.add_entry_widget = createAddEntryWidget()
        self.add_entry_widget.add_button.clicked.connect(self.add_entry)
        layout.addWidget(self.add_entry_widget)

        self.table_preview = TablePreview()
        layout.addWidget(self.table_preview)

        self.setLayout(layout)

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
