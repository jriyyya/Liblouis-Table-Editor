from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit, QLineEdit, QComboBox, QLabel
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from components.ButtonTextInput import ButtonTextInput
from components.OpcodeSelector import OpcodeSelector
from components.UnicodeSelector import UnicodeSelector
from utils.view import clearLayout

def createAddEntryWidget(parent=None):
    widget = QWidget(parent)
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    widget.setStyleSheet("""
        QWidget {
            background-color: #F0F0F0;
            padding: 10px;
            border: 1px solid #DDDDDD;
            border-radius: 5px;
        }
        QTextEdit, QLineEdit, QComboBox {
            background-color: #FFFFFF;
            padding: 5px;
            border: 1px solid #CCCCCC;
            border-radius: 3px;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        QTextEdit::placeholder, QLineEdit::placeholder, QComboBox::placeholder {
            color: #AAAAAA;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 8px 12px;
            border: none;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLabel {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }
    """)

    # Create Opcode input
    input_opcode = ButtonTextInput()
    input_opcode.input.setReadOnly(True)
    input_opcode.input.setPlaceholderText("Select Opcode")
    input_opcode.button.setText("Select")

    def showOpcodePopup():
        def on_select(opcode):
            input_opcode.input.setText(opcode["code"])
            generateForm(opcode["fields"])

        popup = OpcodeSelector()
        popup.on_select(on_select)
        popup.show()

    input_opcode.button.clicked.connect(showOpcodePopup)
    layout.addWidget(input_opcode)

    form_layout = QVBoxLayout()
    layout.addLayout(form_layout)

    def generateForm(fields):
        clearLayout(form_layout)
        for field in fields:
            if field == "characters":
                inp = QTextEdit()
                inp.setPlaceholderText("add characters (string)")
                form_layout.addWidget(inp)

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
                    popup = UnicodeSelector()
                    popup.on_select(lambda char, code: setUnicode(unicode_display, unicode_input, char, code))
                    popup.show()

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

                form_layout.addLayout(unicode_container)

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
                layout.addWidget(dots_type_combo)

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

                form_layout.addLayout(dots_container)

    add_button = QPushButton("Add")
    layout.addWidget(add_button)

    widget.setLayout(layout)
    return widget