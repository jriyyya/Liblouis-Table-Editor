import sys
from utils.view import clearLayout
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from components.UnicodeSelector import UnicodeSelector
from components.OpcodeSelector import OpcodeSelector
from components.ButtonTextInput import ButtonTextInput

from config import WINDOW_WIDTH, WINDOW_HEIGHT 

class TableEntryWidget(QWidget):
    def __init__(self, entry, remove_callback):
        super().__init__()
        layout = QHBoxLayout()

        self.label = QLabel(entry)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(self.label)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.remove_button.setStyleSheet("padding: 4px; margin: 1px;")  # Reduce padding and margin
        layout.addWidget(self.remove_button)

        layout.setContentsMargins(5, 5, 5, 5)  # Remove margins around the layout
        # layout.setSpacing(5)  # Set spacing between widgets

        self.setLayout(layout)

        self.remove_button.clicked.connect(lambda: remove_callback(entry))

class TableManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Liblouis Tables Manager')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.popup = None

        layout = QHBoxLayout()

        # Left panel for table editor
        left_panel = QVBoxLayout()

        self.input_opcode = ButtonTextInput()
        self.input_opcode.input.setReadOnly(True)
        self.input_opcode.input.setPlaceholderText("Select Opcode")
        self.input_opcode.button.setText("Select")
        self.input_opcode.button.clicked.connect(self.showOpcodePopup)

        left_panel.addWidget(self.input_opcode)

        self.form = QVBoxLayout()
        left_panel.addLayout(self.form)

        # Add Button
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.updateTable)
        left_panel.addWidget(add_button)

        left_panel_widget = QWidget()
        left_panel_widget.setLayout(left_panel)

        # Right panel for table display
        right_panel = QVBoxLayout()

        self.table_label = QLabel("Table")
        right_panel.addWidget(self.table_label)

        self.table_lines_list = QListWidget()
        right_panel.addWidget(self.table_lines_list)

        right_panel_widget = QWidget()
        right_panel_widget.setLayout(right_panel)

        # Create QSplitter and add left and right panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel_widget)
        splitter.addWidget(right_panel_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)
        self.setLayout(layout)

        self.selected_opcode = None
        self.table_entries = []

    def showOpcodePopup(self):
        def on_select(opcode):
            self.input_opcode.input.setText(opcode["code"])
            self.selected_opcode = opcode
            self.generateForm(opcode["fields"])

        self.popup = OpcodeSelector()
        self.popup.on_select(on_select)
        self.popup.show()

    def generateForm(self, fields):
        clearLayout(self.form)
        for field in fields:
            if field == "characters":
                inp = QTextEdit()
                inp.setPlaceholderText("add characters (string)")
                self.form.addWidget(inp)

            if field == "unicode":
                inp = ButtonTextInput()
                inp.input.setReadOnly(True)
                inp.input.setPlaceholderText("Select Unicode")
                inp.button.setText("Select")
                i = inp.input
                def open_popup():
                    self.popup = UnicodeSelector()
                    self.popup.on_select(lambda code: i.setText(code))
                    self.popup.show()
                inp.button.clicked.connect(open_popup)
                self.form.addWidget(inp)

            if field == "dots":
                inp = QTextEdit()
                inp.setPlaceholderText("Enter Dots")
                self.form.addWidget(inp)

    def updateTable(self):
        if not self.selected_opcode:
            return

        entry = self.formatEntry()
        if entry:
            self.table_entries.append(entry)
            self.updateTableDisplay()

    def formatEntry(self):
        if not self.selected_opcode:
            return None

        entry = self.selected_opcode["code"]
        for i in range(self.form.count()):
            widget = self.form.itemAt(i).widget()
            if isinstance(widget, QTextEdit) or isinstance(widget, ButtonTextInput):
                text = widget.toPlainText() if isinstance(widget, QTextEdit) else widget.input.text()
                if text.strip():
                    entry += " " + text.strip()
        return entry

    def updateTableDisplay(self):
        self.table_lines_list.clear()
        for entry in self.table_entries:
            item = QListWidgetItem()
            widget = TableEntryWidget(entry, self.removeEntry)
            item.setSizeHint(widget.sizeHint())
            self.table_lines_list.addItem(item)
            self.table_lines_list.setItemWidget(item, widget)

    def removeEntry(self, entry):
        self.table_entries.remove(entry)
        self.updateTableDisplay()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TableManager()
    window.show()

    sys.exit(app.exec_())
