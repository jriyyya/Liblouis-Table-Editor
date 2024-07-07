
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.ApplyStyles import apply_styles

class UnicodeSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Unicode Viewer')
        self.resize(400, 600)

        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search for Unicode / Character")
        self.search.textChanged.connect(self.update_pagination)

        label = QLabel("Double click code to select")

        self.unicodes_list = QListWidget()
        self.unicodes_list.itemDoubleClicked.connect(self.on_item_double_clicked)


        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.page_label)
        button_layout.addWidget(self.next_button)

        layout.addWidget(self.search)
        layout.addWidget(label)
        layout.addWidget(self.unicodes_list)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.full_unicode_list = []
        self.filtered_unicode_list = []
        self.current_page = 1
        self.items_per_page = 50  # Adjust as needed
        self.populate_full_list()
        self.update_pagination()
        apply_styles(self)

    def populate_full_list(self):
        self.full_unicode_list = [
            (chr(code), f"\\x{code:04X}", f"{chr(code)} (U+{code:04X})")
            for code in range(0x0000, 0xFFFF)
        ]

    def filter_list(self):
        search_text = self.search.text().lower()
        self.filtered_unicode_list = [
            item for item in self.full_unicode_list
            if search_text in item[0].lower() or search_text in item[1].lower()
        ]

    def update_list(self):
        self.unicodes_list.clear()
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = self.current_page * self.items_per_page

        for char, unicode_code, _ in self.filtered_unicode_list[start_index:end_index]:
            display_text = f"{char} (\\x{ord(char):04X})"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, (char, unicode_code))
            self.unicodes_list.addItem(item)
            
    def update_pagination(self):
        self.filter_list()
        total_pages = math.ceil(len(self.filtered_unicode_list) / self.items_per_page)
        if total_pages == 0:
            total_pages = 1  # Ensure at least 1 page
        self.current_page = min(self.current_page, total_pages)
        self.page_label.setText(f"Page {self.current_page} / {total_pages}")
        self.update_list()

    def previous_page(self):
        self.current_page = max(1, self.current_page - 1)
        self.update_pagination()

    def next_page(self):
        total_pages = math.ceil(len(self.filtered_unicode_list) / self.items_per_page)
        self.current_page = min(total_pages, self.current_page + 1)
        self.update_pagination()

    def on_item_double_clicked(self, item):
        if self.callback:
            char, code = item.data(Qt.UserRole)
            self.callback(char, code)
        self.hide()

    def on_select(self, cb):
        self.callback = cb
