from PyQt5.QtWidgets import QTextEdit

class TablePreview(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Table Preview")
        self.setReadOnly(True)

    def add_entry(self, entry):
        current_content = self.toPlainText()
        new_content = f"{current_content}\n{entry}".strip()
        self.setPlainText(new_content)
