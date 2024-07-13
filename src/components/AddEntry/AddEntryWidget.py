from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit, QLineEdit, QComboBox, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator

from components.ButtonTextInput import ButtonTextInput
from components.OpcodeSelector import OpcodeSelector
from components.UnicodeSelector import UnicodeSelector
from utils.view import clearLayout
from utils.ApplyStyles import apply_styles

class AddEntryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        self.input_opcode = ButtonTextInput()
        self.input_opcode.input.setReadOnly(True)
        self.input_opcode.input.setPlaceholderText("Select Opcode")
        self.input_opcode.button.setText("Select")

        opcode_layout = QHBoxLayout()

        self.input_opcode.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        opcode_layout.addWidget(self.input_opcode.input)
        opcode_layout.addWidget(self.input_opcode.button)

        layout.addLayout(opcode_layout)

        self.input_opcode.button.clicked.connect(self.showOpcodePopup)

        self.form_layout = QVBoxLayout()
        layout.addLayout(self.form_layout)

        self.add_button = QPushButton("Add")
        layout.addWidget(self.add_button, alignment=Qt.AlignTop)

        self.setLayout(layout)
        apply_styles(self)

    def showOpcodePopup(self):
        def on_select(opcode):
            self.input_opcode.input.setText(opcode["code"])
            self.generateForm(opcode["fields"])

        self.popup = OpcodeSelector()
        self.popup.on_select(on_select)
        self.popup.show()

    def generateForm(self, fields):
        clearLayout(self.form_layout)
        for field in fields:
            if field == "characters":
                inp = QTextEdit()
                inp.setPlaceholderText("add characters (string)")
                self.form_layout.addWidget(inp)

            elif field == "unicode":
                def updateUnicodeInput(text, unicode_input):
                    if text:
                        unicode_input.setText('\\x' + '{:04X}'.format(ord(text)))
                    else:
                        unicode_input.clear()

                def updateDisplayCharacter(unicode_display, text):
                    try:
                        char = chr(int(text.replace('\\x', ''), 16))
                        unicode_display.setText(char)
                    except ValueError:
                        unicode_display.clear()

                def showUnicodePopup(unicode_display, unicode_input):
                    self.unicode_popup = UnicodeSelector()
                    self.unicode_popup.on_select(lambda char, code: setUnicode(unicode_display, unicode_input, char, code))
                    self.unicode_popup.show()

                def setUnicode(unicode_display, unicode_input, char, code):
                    unicode_display.setText(char)
                    code_value = int(code[2:], 16)
                    unicode_input.setText(f"\\x{code_value:04X}")

                unicode_container = QHBoxLayout()
                unicode_display = QLineEdit()
                unicode_display.setPlaceholderText("Selected Character")
                unicode_display.setMaxLength(1)
                unicode_input = QLineEdit()
                unicode_input.setPlaceholderText("Unicode Value")
                unicode_input.setProperty("includeInEntry", True)

                unicode_input.textChanged.connect(lambda text: updateDisplayCharacter(unicode_display, text))
                unicode_display.textChanged.connect(lambda text: updateUnicodeInput(text, unicode_input))

                select_button = QPushButton("Select Unicode")
                select_button.clicked.connect(lambda: showUnicodePopup(unicode_display, unicode_input))

                unicode_container.addWidget(unicode_display)
                unicode_container.addWidget(unicode_input)
                unicode_container.addWidget(select_button)

                self.form_layout.addLayout(unicode_container)

            elif field == "dots":
                def updateBrailleDotsDisplay():
                    text = dots_input.text()
                    text = ''.join(sorted(set(text)))  # Remove duplicates and sort
                    if not text.isdigit():
                        dots_input.setText('')
                        resetBrailleDotsDisplay()
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

                    dots_display.setText(
                        f"{braille_representation[0][0]} {braille_representation[0][1]}\n"
                        f"{braille_representation[1][0]} {braille_representation[1][1]}\n"
                        f"{braille_representation[2][0]} {braille_representation[2][1]}"
                    )

                def resetBrailleDotsDisplay():
                    dots_display.setText("○ ○\n○ ○\n○ ○")

                def updateDotsInputPlaceholder(text):
                    nonlocal dots_input  # Ensure dots_input is accessible from this function
                    if "6 dots" in text:
                        dots_input.setPlaceholderText("Enter Dots (1-6)")
                    else:
                        dots_input.setPlaceholderText("Enter Dots (1-8)")

                dots_type_combo = QComboBox()
                dots_type_combo.addItems(["Standard Braille (6 dots)", "Extended Braille (8 dots)"])
                dots_type_combo.currentTextChanged.connect(updateDotsInputPlaceholder)
                self.form_layout.addWidget(dots_type_combo)

                dots_container = QHBoxLayout()

                dots_input = QLineEdit()
                dots_input.setPlaceholderText("Enter Dots (1-6)")
                dots_input.setValidator(QRegExpValidator(QRegExp("^(?=\\d{1,6}$)1?2?3?4?5?6?$")))
                dots_input.setProperty("includeInEntry", True)
                dots_input.textChanged.connect(updateBrailleDotsDisplay)
                dots_container.addWidget(dots_input, 1)

                dots_display = QLabel()
                dots_display.setAlignment(Qt.AlignCenter)
                dots_display.setText("○ ○\n○ ○\n○ ○")  # Default empty dots representation
                dots_container.addWidget(dots_display, 1)

                self.form_layout.addLayout(dots_container)

def createAddEntryWidget(parent=None):
    return AddEntryWidget(parent)
