import sys
import os
import re
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
        self.remove_button.setStyleSheet("padding: 4px; margin: 1px;")
        layout.addWidget(self.remove_button)

        layout.setContentsMargins(5, 5, 5, 5)
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
        left_panel.setAlignment(Qt.AlignTop | Qt.AlignLeft)

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

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_table)
        right_panel.addWidget(save_button)

        load_button = QPushButton("Load Table")
        load_button.clicked.connect(self.load_table)
        right_panel.addWidget(load_button)

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
                unicode_container = QHBoxLayout()

                unicode_display = QLineEdit()
                unicode_display.setPlaceholderText("Selected Character")
                unicode_display.setMaxLength(1)
                unicode_display.textChanged.connect(lambda text: self.updateUnicodeInput(text, unicode_input))

                unicode_input = QLineEdit()
                unicode_input.setPlaceholderText("Unicode Value")
                unicode_input.setProperty("includeInEntry", True)
                unicode_input.textChanged.connect(lambda text: self.updateDisplayCharacter(unicode_display, text))

                select_button = QPushButton("Select Unicode")
                select_button.clicked.connect(lambda: self.showUnicodePopup(unicode_display, unicode_input))

                unicode_container.addWidget(unicode_display)
                unicode_container.addWidget(unicode_input)
                unicode_container.addWidget(select_button)

                self.form.addLayout(unicode_container)

            if field == "dots":
                self.dots_type_combo = QComboBox()
                self.dots_type_combo.addItems(["Standard Braille (6 dots)", "Extended Braille (8 dots)"])
                self.dots_type_combo.currentTextChanged.connect(self.updateDotsInputPlaceholder)
                self.form.addWidget(self.dots_type_combo)

                dots_container = QHBoxLayout()

                self.dots_input = QLineEdit()
                self.dots_input.setPlaceholderText("Enter Dots (1-6)")
                self.dots_input.setValidator(QRegExpValidator(QRegExp("^(?=\\d{1,6}$)1?2?3?4?5?6?$")))
                self.dots_input.setProperty("includeInEntry", True)
                self.dots_input.textChanged.connect(self.updateBrailleDotsDisplay)
                dots_container.addWidget(self.dots_input, 1)

                self.dots_display = QLabel()
                self.dots_display.setAlignment(Qt.AlignCenter)
                self.dots_display.setText("○ ○\n○ ○\n○ ○")  # Default empty dots representation
                dots_container.addWidget(self.dots_display, 1)

                self.form.addLayout(dots_container)


    def showUnicodePopup(self, unicode_display, unicode_input):
        self.popup = UnicodeSelector()
        self.popup.on_select(lambda char, code: self.setUnicode(unicode_display, unicode_input, char, code))
        self.popup.show()

    def setUnicode(self, unicode_display, unicode_input, char, code):
        unicode_display.setText(char)
        code_value = int(code[2:], 16)
        unicode_input.setText(f"\\x{code_value:04X}")  # Format the integer as a hexadecimal string
    

    def updateUnicodeInput(self, text, unicode_input):
        if text:
            unicode_input.setText('\\x' + '{:04X}'.format(ord(text)))
        else:
            unicode_input.clear()

    def updateDisplayCharacter(self, unicode_display, text):
        try:
            char = chr(int(text.replace('\\x', ''), 16))
            unicode_display.setText(char)
        except ValueError:
            unicode_display.clear()

    def updateDotsInputPlaceholder(self, text):
        if "6 dots" in text:
            self.dots_input.setPlaceholderText("Enter Dots (1-6)")
        else:
            self.dots_input.setPlaceholderText("Enter Dots (1-8)")

    def updateBrailleDotsDisplay(self):
        text = self.dots_input.text()
        text = ''.join(sorted(set(text)))  # Remove duplicates and sort
        if not text.isdigit():
            self.dots_input.setText('')
            self.resetBrailleDotsDisplay()
            return
        dots = [int(d) for d in text if d in '123456']

        braille_representation = [['○', '○'], ['○', '○'], ['○', '○']]
        if 1 in dots:
            braille_representation[0][0] = '●'
        if 2 in dots:
            braille_representation[1][0] = '●'
        if 3 in dots:
            braille_representation[2][0] = '●'
        if 4 in dots:
            braille_representation[0][1] = '●'
        if 5 in dots:
            braille_representation[1][1] = '●'
        if 6 in dots:
            braille_representation[2][1] = '●'

        self.dots_display.setText(
            f"{braille_representation[0][0]} {braille_representation[0][1]}\n"
            f"{braille_representation[1][0]} {braille_representation[1][1]}\n"
            f"{braille_representation[2][0]} {braille_representation[2][1]}"
        )
    
    def resetBrailleDotsDisplay(self):
        self.dots_display.setText("○ ○\n○ ○\n○ ○")

    def updateTable(self):
        if not self.selected_opcode:
            return

        entry = self.formatEntry()
        if entry:
            if entry in self.table_entries:
                QMessageBox.warning(self, "Duplicate Entry", "The entry is already in the table.")
            else:
                self.table_entries.append(entry)
                self.updateTableDisplay()

    def formatEntry(self):
        if not self.selected_opcode:
            return None

        entry = self.selected_opcode["code"]

        def traverse_layout(layout):
            nonlocal entry
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                if widget:
                    if isinstance(widget, QTextEdit):
                        text = widget.toPlainText()
                        if text.strip():
                            entry += " " + text.strip()
                    elif isinstance(widget, QLineEdit):
                        if not widget.isReadOnly() and widget.property("includeInEntry") and widget.text().strip():
                            entry += " " + widget.text().strip()
                elif item.layout():
                    traverse_layout(item.layout())

        traverse_layout(self.form)
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

    def save_table(self):
        table_text = "\n".join(self.table_lines_list.itemWidget(self.table_lines_list.item(index)).label.text() for index in range(self.table_lines_list.count()))
        file_path = os.path.join(os.path.dirname(__file__), "assets", "data", "table.txt")
        with open(file_path, "w") as file:
            file.write(table_text)

        QMessageBox.information(self, "Table Saved", "Table saved as table.txt")

        # Clear the table entries
        self.table_entries.clear()
        self.updateTableDisplay()

    def load_table(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Table", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                table_text = file.read()
                self.populate_table(table_text)

    def populate_table(self, table_text):
        entries = table_text.split("\n")
        self.table_entries.extend(entries)
        self.updateTableDisplay()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TableManager()
    window.show()

    sys.exit(app.exec_())
