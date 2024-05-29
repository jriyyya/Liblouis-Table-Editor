from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class UnicodeSelector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Unicode Viewer')
        self.resize(400, 600)

        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search for Unicode / Character")
        self.search.textChanged.connect(self.filter_list)

        label = QLabel("Double click code to select")

        self.unicodes_list = QListWidget()
        self.unicodes_list.itemDoubleClicked.connect(self.on_item_double_clicked)

        layout.addWidget(self.search)
        layout.addWidget(label)
        layout.addWidget(self.unicodes_list)

        self.setLayout(layout)

        self.full_unicode_list = []
        self.filtered_unicode_list = []
        self.callback = None
        self.populate_full_list()
        self.filter_list()

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
        self.update_list()

    def update_list(self):
        self.unicodes_list.clear()
        for char, unicode_code, display_text in self.filtered_unicode_list[:1000]:
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, (char, unicode_code))
            self.unicodes_list.addItem(item)

    def on_item_double_clicked(self, item):
        if self.callback:
            char, code = item.data(Qt.UserRole)
            self.callback(char, code)
        self.hide()

    def on_select(self, cb):
        self.callback = cb
