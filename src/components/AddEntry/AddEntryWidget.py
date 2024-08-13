from collections import OrderedDict
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QComboBox, QLabel, QPushButton, QSizePolicy, QLayout
)
from PyQt5.QtCore import Qt
from components.AddEntry.BrailleInputWidget import BrailleInputWidget
from components.AddEntry.UnicodeSelector import UnicodeSelector
from utils.view import clearLayout

data = json.load(open('./src/assets/data/opcodes.json', 'r'), object_pairs_hook=OrderedDict)
opcodes = data["codes"]

class OpcodeForm(QWidget):
    def __init__(self, fields, parent=None):
        super().__init__(parent)
        self.field_inputs = {}
        self.initUI(fields)

    def initUI(self, fields):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.form_layout = QVBoxLayout()
        layout.addLayout(self.form_layout)

        self.nested_forms = []  # Track nested forms

        for field, placeholder in fields.items():
            if field == "opcode":
                nested_opcode_combo = QComboBox()
                nested_opcode_combo.setPlaceholderText("Select Opcode")
                self.populate_opcode_combo(nested_opcode_combo)
                nested_opcode_combo.currentIndexChanged.connect(
                    lambda idx, combo=nested_opcode_combo: self.on_opcode_selected(idx, combo)
                )
                self.form_layout.addWidget(nested_opcode_combo)
                self.field_inputs[field] = nested_opcode_combo

            elif field == "unicode" or field.startswith("unicode"):
                unicode_container = QHBoxLayout()
                unicode_display = QLineEdit()
                unicode_display.setPlaceholderText("Selected Character")
                unicode_input = QLineEdit()
                unicode_input.setPlaceholderText(placeholder)
                unicode_input.setProperty("includeInEntry", True)
                
                # Set size policy for full width
                unicode_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                unicode_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                unicode_input.textChanged.connect(lambda text, u_display=unicode_display: self.updateDisplayCharacter(u_display, text))
                unicode_display.textChanged.connect(lambda text, u_input=unicode_input: self.updateUnicodeInput(text, u_input))

                select_button = QPushButton("Select Unicode")
                select_button.clicked.connect(lambda _, u_display=unicode_display, u_input=unicode_input: self.showUnicodePopup(u_display, u_input))

                unicode_container.addWidget(unicode_display)
                unicode_container.addWidget(unicode_input)
                unicode_container.addWidget(select_button)
                
                # Ensure container uses full width
                unicode_container.setSizeConstraint(QLayout.SetMinimumSize)

                self.form_layout.addLayout(unicode_container)
                self.field_inputs[field] = unicode_input

            elif field == "name":
                name_input = QLineEdit()
                name_input.setPlaceholderText(placeholder)
                # Set size policy for full width
                name_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.form_layout.addWidget(name_input)
                self.field_inputs[field] = name_input

            elif field == "characters":
                inp = QTextEdit()
                inp.setPlaceholderText(placeholder)
                # Set size policy for full width
                inp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.form_layout.addWidget(inp)
                self.field_inputs[field] = inp

            elif field == "dots":
                self.braille_input_widget = BrailleInputWidget()
                self.form_layout.addWidget(self.braille_input_widget)
                self.field_inputs[field] = self.braille_input_widget.braille_input

            elif field == "base_attribute":
                base_attr_dropdown = QComboBox()
                base_attr_dropdown.addItems(["space", "digit", "letter", "lowercase", "uppercase", "punctuation", "sign", "math", "litdigit", "attribute", "before", "after"])
                # Set size policy for full width
                base_attr_dropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                self.form_layout.addWidget(base_attr_dropdown)
                self.field_inputs[field] = base_attr_dropdown

    def populate_opcode_combo(self, combo):
        combo.clear()
        combo.addItem("Select Opcode", None)  # Default placeholder item
        for opcode in opcodes:
            combo.addItem(opcode["code"], opcode)

    def on_opcode_selected(self, index, combo):
        if index > 0:
            opcode = combo.itemData(index)
            self.clear_nested_forms()  # Clear previously added nested forms
            nested_form = OpcodeForm(opcode["fields"], self)
            self.form_layout.addWidget(nested_form)
            self.nested_forms.append(nested_form)
        else:
            clearLayout(self.form_layout)

    def clear_nested_forms(self):
        for form in self.nested_forms:
            form.deleteLater()  # Remove from layout
        self.nested_forms.clear()  # Clear list

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


class AddEntryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.field_inputs = {}
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        self.opcode_combo_layout = QHBoxLayout()

        self.opcode_combo = QComboBox()
        self.opcode_combo.setPlaceholderText("Select Opcode")
        self.populate_opcode_combo()
        self.opcode_combo.currentIndexChanged.connect(self.on_opcode_selected)
        self.opcode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.opcode_combo_layout.addWidget(self.opcode_combo)
        main_layout.addLayout(self.opcode_combo_layout)

        self.form_layout = QVBoxLayout()
        main_layout.addLayout(self.form_layout)

        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Add a comment (optional)")
        # Set size policy for full width
        self.comment_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        main_layout.addWidget(self.comment_input)

        self.add_button = QPushButton("Add")
        main_layout.addWidget(self.add_button, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

    def populate_opcode_combo(self, combo=None):
        if combo is None:
            combo = self.opcode_combo
        combo.clear()
        combo.addItem("Select Opcode", None)  # Default placeholder item
        for opcode in opcodes:
            combo.addItem(opcode["code"], opcode)

    def on_opcode_selected(self, index):
        clearLayout(self.form_layout)  # Clear previous forms
        if index > 0:
            opcode = self.opcode_combo.itemData(index)
            nested_form = OpcodeForm(opcode["fields"], self)
            self.form_layout.addWidget(nested_form)
            self.field_inputs["nested_form"] = nested_form

    def collect_entry_data(self):
        collected_data = [self.opcode_combo.currentText()]
        
        for field_input in self.field_inputs.values():
            if isinstance(field_input, QLineEdit) or isinstance(field_input, QTextEdit):
                collected_data.append(field_input.text())
            elif isinstance(field_input, QComboBox):
                collected_data.append(field_input.currentText())
            elif isinstance(field_input, BrailleInputWidget):
                collected_data.append(field_input.braille_input.text())
        
        collected_data.append(self.comment_input.text())
        
        return ' '.join(collected_data).strip()
