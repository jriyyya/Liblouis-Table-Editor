import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeWidget, QTreeWidgetItem, QGridLayout, QScrollArea, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class UnicodeSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Unicode Character Map')
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Unicode Blocks")
        self.populate_tree()
        self.tree.itemClicked.connect(self.display_characters)
        self.tree.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addWidget(self.tree)

        scroll_area = QScrollArea()
        self.char_container = QWidget()
        self.char_layout = QGridLayout(self.char_container)
        self.char_layout.setContentsMargins(0, 0, 0, 0)
        self.char_layout.setSpacing(0)
        self.char_container.setStyleSheet("background: white;")
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.char_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

        self.setFixedSize(920, 600)

        self.adjust_component_sizes()

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
        return {
            "Basic Latin": (0x0000, 0x007F),
            "Latin-1 Supplement": (0x0080, 0x00FF),
            "Latin Extended-A": (0x0100, 0x017F),
            "Latin Extended-B": (0x0180, 0x024F),
            "IPA Extensions": (0x0250, 0x02AF),
            "Spacing Modifier Letters": (0x02B0, 0x02FF),
            "Greek and Coptic": (0x0370, 0x03FF),
            "Cyrillic": (0x0400, 0x04FF),
            "Hindi": (0x0900, 0x097F),
        }

    def display_characters(self, item, column):
        while self.char_layout.count():
            child = self.char_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        start, end = item.data(0, Qt.UserRole)
        characters = [chr(codepoint) for codepoint in range(start, end + 1)]

        button_size = 60
        num_columns = 10
        padding = 0

        num_rows = (len(characters) + num_columns - 1) // num_columns

        container_width = num_columns * (button_size + padding) - padding
        container_height = num_rows * (button_size + padding) - padding

        available_width = self.width() - self.tree.sizeHint().width()
        container_width = min(container_width, available_width)

        self.char_container.setFixedSize(container_width, container_height)

        for row in range(num_rows):
            for col in range(num_columns):
                index = row * num_columns + col
                if index >= len(characters):
                    break

                char = characters[index]
                char_button = QPushButton(char)
                char_button.setFont(QFont('Sans', 16))
                char_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                char_button.setFixedSize(QSize(button_size, button_size))

                char_button.setStyleSheet(
                    "QPushButton {"
                    "    border: 1px solid #b0c6cf;"
                    "    background: white;"
                    "}"
                    "QPushButton:hover {"
                    "    background: #d4e9f7;"
                    "}"
                )
                char_button.clicked.connect(self.character_selected)
                self.char_layout.addWidget(char_button, row, col)

    def character_selected(self):
        char_button = self.sender()
        selected_char = char_button.text()
        self.on_select_callback(selected_char, f"\\x{ord(selected_char):04X}")
        self.close()

    def on_select(self, callback):
        self.on_select_callback = callback

    def adjust_component_sizes(self):
        self.tree.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.char_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
