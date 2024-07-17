from PyQt5.QtWidgets import QTextEdit, QMenu, QAction
from PyQt5.QtCore import Qt

class TablePreview(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

        self.entries = []
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def add_entry(self, entry):
        self.entries.append(entry)
        self.update_content()

    def update_content(self):
        new_content = "\n".join(
            f"{entry['opcode']} {entry.get('unicode', '')} {entry.get('dots', '')} {entry.get('comment', '')}"
            for entry in self.entries
        )
        self.setPlainText(new_content)

    def showContextMenu(self, pos):
        cursor = self.cursorForPosition(pos)
        cursor.select(cursor.LineUnderCursor)
        selected_text = cursor.selectedText()

        menu = QMenu(self)

        duplicate_action = QAction('Duplicate', self)
        duplicate_action.triggered.connect(lambda: self.duplicate_entry(selected_text))
        menu.addAction(duplicate_action)

        edit_action = QAction('Edit', self)
        edit_action.triggered.connect(lambda: self.edit_entry(selected_text))
        menu.addAction(edit_action)

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(lambda: self.delete_entry(selected_text))
        menu.addAction(delete_action)

        menu.exec_(self.mapToGlobal(pos))

    def duplicate_entry(self, entry_text):
        for entry in self.entries:
            if self.entry_to_text(entry) == entry_text:
                duplicated_entry = entry.copy()
                self.entries.append(duplicated_entry)
                self.update_content()
                break

    def edit_entry(self, entry_text):
        # Implement editing logic here
        pass

    def delete_entry(self, entry_text):
        self.entries = [entry for entry in self.entries if self.entry_to_text(entry) != entry_text]
        self.update_content()

    def entry_to_text(self, entry):
        return f"{entry['opcode']} {entry.get('unicode', '')} {entry.get('dots', '')} {entry.get('comment', '')}"
