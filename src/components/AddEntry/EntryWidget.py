from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt

class EntryWidget(QWidget):
    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.initUI()

    def initUI(self):
        entry_text = f"{self.entry['opcode']} {self.entry.get('unicode', '')} {self.entry.get('braille', '')} {self.entry.get('comment', '')}"

        self.label_text = QLabel(entry_text)
        self.label_text.setWordWrap(True)

        layout = QHBoxLayout(self)
        layout.addWidget(self.label_text, alignment=Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Set initial border style
        self.setStyleSheet("border: 1px solid #b0c6cf; border-radius: 5px; padding: 10px;; background-color: white;")
        
        # Connect hover events
        self.setMouseTracking(True)
        self.enterEvent = self.onHoverEnter
        self.leaveEvent = self.onHoverLeave

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        duplicate_action = QAction('Duplicate', self)
        duplicate_action.triggered.connect(self.duplicate_entry)
        menu.addAction(duplicate_action)

        edit_action = QAction('Edit', self)
        edit_action.triggered.connect(self.edit_entry)
        menu.addAction(edit_action)

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.delete_entry)
        menu.addAction(delete_action)

        menu.exec_(self.mapToGlobal(event.pos()))

    def duplicate_entry(self):
        new_entry_widget = EntryWidget(self.entry, parent=self.parentWidget())
        self.parentWidget().layout().insertWidget(self.parentWidget().layout().indexOf(self) + 1, new_entry_widget)

    def edit_entry(self):
        pass

    def delete_entry(self):
        self.setParent(None)
        self.deleteLater()

    def onHoverEnter(self, event):
        self.setStyleSheet("border: 1px solid #b0c6cf; border-radius: 5px; padding: 10px; background-color: #f0f8ff;")

    def onHoverLeave(self, event):
        self.setStyleSheet("border: 1px solid #b0c6cf; border-radius: 5px; padding: 10px; background-color: white;")
