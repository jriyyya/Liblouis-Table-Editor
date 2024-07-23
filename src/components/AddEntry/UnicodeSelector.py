import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QTextEdit,
    QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt

class UnicodeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Unicode Character Map')
        self.resize(800, 600)
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        # Create tree view for Unicode blocks
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Unicode Blocks")
        self.populate_tree()
        self.tree.itemClicked.connect(self.display_characters)
        layout.addWidget(self.tree, 1)

        # Create text widget to display characters
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setFontPointSize(20)
        self.text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text.mouseDoubleClickEvent = self.character_selected
        layout.addWidget(self.text, 2)

        self.setLayout(layout)

        # Select the first item by default
        if self.tree.topLevelItemCount() > 0:
            first_item = self.tree.topLevelItem(0)
            self.tree.setCurrentItem(first_item)
            self.display_characters(first_item, 0)

    def populate_tree(self):
        blocks = self.get_unicode_blocks()
        for block_name, (start, end) in blocks.items():
            item = QTreeWidgetItem([block_name])
            item.setData(0, Qt.UserRole, (start, end))
            self.tree.addTopLevelItem(item)

    def get_unicode_blocks(self):
        # This is a predefined list of Unicode blocks
        return {
            "Basic Latin": (0x0000, 0x007F),
            "Latin-1 Supplement": (0x0080, 0x00FF),
            "Latin Extended-A": (0x0100, 0x017F),
            "Latin Extended-B": (0x0180, 0x024F),
            "IPA Extensions": (0x0250, 0x02AF),
            "Spacing Modifier Letters": (0x02B0, 0x02FF),
            "Greek and Coptic": (0x0370, 0x03FF),
            "Cyrillic": (0x0400, 0x04FF),
            # Add more blocks as needed
        }

    def display_characters(self, item, column):
        self.text.clear()
        start, end = item.data(0, Qt.UserRole)
        characters = ''.join(chr(codepoint) for codepoint in range(start, end + 1))
        self.text.setText(characters)

    def character_selected(self, event):
        cursor = self.text.cursorForPosition(event.pos())
        cursor.select(cursor.WordUnderCursor)
        selected_char = cursor.selectedText()
        self.on_select_callback(selected_char, f"\\x{ord(selected_char):04X}")
        self.close()

    def on_select(self, callback):
        self.on_select_callback = callback

