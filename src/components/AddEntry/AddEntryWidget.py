import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QComboBox, QLabel, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from components.AddEntry.BrailleInputWidget import BrailleInputWidget
from components.AddEntry.UnicodeSelector import UnicodeSelector
from utils.view import clearLayout
from utils.ApplyStyles import apply_styles

data = json.load(open('./src/assets/data/opcodes.json', 'r'))
opcodes = data["codes"]

class AddEntryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.opcode_combo = QComboBox()
        self.opcode_combo.setPlaceholderText("Select Opcode")
        self.populate_opcode_combo()
        self.opcode_combo.currentIndexChanged.connect(self.on_opcode_selected)

        opcode_layout = QHBoxLayout()
        self.opcode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        opcode_layout.addWidget(self.opcode_combo)
        layout.addLayout(opcode_layout)

        self.form_layout = QVBoxLayout()
        layout.addLayout(self.form_layout)
        
        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Add a comment (optional)")
        layout.addWidget(self.comment_input)

        self.add_button = QPushButton("Add")
        layout.addWidget(self.add_button, alignment=Qt.AlignTop)

        self.setLayout(layout)
        apply_styles(self)

    def populate_opcode_combo(self):
        self.opcode_combo.clear()
        self.opcode_combo.addItem("Select Opcode", None)  # Default placeholder item
        for opcode in opcodes:
            self.opcode_combo.addItem(opcode["code"], opcode)

    def on_opcode_selected(self, index):
        if index > 0:  # Ignore the placeholder item
            opcode = self.opcode_combo.itemData(index)
            self.generateForm(opcode["fields"])
        else:
            clearLayout(self.form_layout)

    def generateForm(self, fields):
        clearLayout(self.form_layout)
        self.field_inputs = {}

        for field in fields:
            if field == "characters":
                inp = QTextEdit()
                inp.setPlaceholderText("Add characters (string)")
                self.form_layout.addWidget(inp)
                self.field_inputs[field] = inp

            elif field == "unicode":
                unicode_container = QHBoxLayout()
                unicode_display = QLineEdit()
                unicode_display.setPlaceholderText("Selected Character")
                unicode_input = QLineEdit()
                unicode_input.setPlaceholderText("Unicode Value")
                unicode_input.setProperty("includeInEntry", True)

                unicode_input.textChanged.connect(lambda text, u_display=unicode_display: self.updateDisplayCharacter(u_display, text))
                unicode_display.textChanged.connect(lambda text, u_input=unicode_input: self.updateUnicodeInput(text, u_input))

                select_button = QPushButton("Select Unicode")
                select_button.clicked.connect(lambda _, u_display=unicode_display, u_input=unicode_input: self.showUnicodePopup(u_display, u_input))

                unicode_container.addWidget(unicode_display)
                unicode_container.addWidget(unicode_input)
                unicode_container.addWidget(select_button)

                self.form_layout.addLayout(unicode_container)
                self.field_inputs[field] = unicode_input

            elif field == "dots":
                self.braille_input_widget = BrailleInputWidget()
                self.form_layout.addWidget(self.braille_input_widget)
                self.field_inputs[field] = self.braille_input_widget.braille_input

    def collect_entry_data(self):
        entry_data = {
            "opcode": self.opcode_combo.currentText()
        }
        for field, field_input in self.field_inputs.items():
            entry_data[field] = field_input.text()
        comment = self.comment_input.text()
        if comment:
            entry_data["comment"] = comment
        return entry_data

    def updateUnicodeInput(self, text, unicode_input):
        if text:
            hex_values = [f'\\x{ord(char):04X}' for char in text]
            unicode_input.setText(''.join(hex_values))
        else:
            unicode_input.clear()

    def updateDisplayCharacter(self, unicode_display, text):
        try:
            characters = []
            hex_values = text.split('\\x')[1:]

            for hex_value in hex_values:
                if hex_value:
                    hex_value = hex_value.zfill(4)
                    code_point = int(hex_value, 16)
                    if code_point > 0x10FFFF:
                        raise ValueError(f"Code point {hex_value} is too large to be a valid Unicode character.")
                    characters.append(chr(code_point))

            unicode_display.setText("".join(characters))
        
        except (ValueError, OverflowError) as e:
            unicode_display.setText("[Invalid Unicode]")
            print(f"Error converting Unicode: {e}")




    def showUnicodePopup(self, unicode_display, unicode_input):
        self.unicode_popup = UnicodeSelector()
        self.unicode_popup.on_select(lambda char, code: self.setUnicode(unicode_display, unicode_input, char, code))
        self.unicode_popup.show()
        
    def setUnicode(self, unicode_display, unicode_input, char, code):
        unicode_display.setText(char)
        unicode_input.setText(code)
