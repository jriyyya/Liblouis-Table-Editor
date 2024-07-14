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
        new_content = "\n".join(self.entries)
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

    def duplicate_entry(self, entry):
        self.add_entry(entry)

    def edit_entry(self, entry):
        self.delete_entry(entry)
        self.parent().parent().add_entry_widget.input_opcode.input.setText(entry)

    def delete_entry(self, entry):
        if entry in self.entries:
            self.entries.remove(entry)
            self.update_content()
