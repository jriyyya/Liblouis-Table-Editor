from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QTextEdit
from utils.ApplyStyles import apply_styles
from components.AddEntry.AddEntryWidget import createAddEntryWidget
from components.TablePreview import TablePreview  # Assuming TablePreview is in components.TablePreview

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
        top_layout.addWidget(self.add_entry_widget)

        self.add_entry_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addLayout(top_layout)

        self.testing = QTextEdit(self)
        self.testing.setPlaceholderText("Testing")
        main_layout.addWidget(self.testing)

        self.setLayout(main_layout)

        apply_styles(self)

        self.add_entry_widget.add_button.clicked.connect(self.add_entry_to_table)

    def add_entry_to_table(self):
        entry_data = self.add_entry_widget.collect_entry_data()
        formatted_entry = ' '.join(entry_data)
        self.table_preview.add_entry(formatted_entry)

    def set_content(self, content):
        self.table_preview.setPlainText(content)

    def add_tab(self, file_name, content):
        new_tab = QWidget(self)
        layout = QVBoxLayout(new_tab)

        table_preview = TablePreview(self)
        table_preview.setPlainText(content)
        layout.addWidget(table_preview)

        new_tab.setLayout(layout)
        self.tab_widget.addTab(new_tab, file_name)
