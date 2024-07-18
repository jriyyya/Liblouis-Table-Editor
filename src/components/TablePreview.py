from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt
from components.AddEntry.EntryWidget import EntryWidget
from utils.ApplyStyles import apply_styles

class TablePreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.entries = []
        apply_styles(self)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white; border: none;")  # Set white background and no border
        
        self.layout = QVBoxLayout(self)
        
        # Create a scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        
        # Container widget for scroll area contents
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)  # Align widgets to the top
        
        self.scroll_area.setWidget(self.scroll_widget)
        
        # Add the scroll area to the main layout
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

    def add_entry(self, entry):
        self.entries.append(entry)
        self.update_content()

    def update_content(self):
        self.clear_layout()

        for entry in self.entries:
            entry_widget = EntryWidget(entry)
            self.scroll_layout.addWidget(entry_widget)

    def clear_layout(self):
        # Clear all widgets from the scroll layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
