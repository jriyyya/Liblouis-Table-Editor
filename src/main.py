import sys
from utils.view import clearLayout
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from components.UnicodeSelector import UnicodeSelector
from components.OpcodeSelector import OpcodeSelector
from components.ButtonTextInput import ButtonTextInput

from config import WINDOW_WIDTH, WINDOW_HEIGHT 

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
        self.input_opcode.button.clicked.connect(lambda : self.showOpcodePopup())

        left_panel.addWidget(self.input_opcode)

        self.form = QVBoxLayout()
        left_panel.addLayout(self.form)

        # Add Button
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.updateTable)
        left_panel.addWidget(add_button)

        # Right panel for table display
        right_panel = QVBoxLayout()

        self.table_label = QLabel("Table")
        right_panel.addWidget(self.table_label)

        self.table_lines_list = QListWidget()
        right_panel.addWidget(self.table_lines_list)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(QWidget())  # Placeholder for future expansion
        splitter.addWidget(QWidget())  # Placeholder for future expansion

        splitter.setStretchFactor(0, 1)  # Make left panel stretchable
        splitter.setStretchFactor(1, 0)  # Make right panel non-stretchable

        layout.addWidget(splitter)

        left_panel_widget = QWidget()
        left_panel_widget.setLayout(left_panel)
        right_panel_widget = QWidget()
        right_panel_widget.setLayout(right_panel)

        splitter.widget(0).setLayout(left_panel.layout())
        splitter.widget(1).setLayout(right_panel.layout())

        self.setLayout(layout)

        self.selected_opcode = None
        self.table_entries = []

    def showOpcodePopup(self):
        def on_select(opcode):
            self.input_opcode.input.setText(opcode["code"])
            self.selected_opcode = opcode
            self.generateForm(opcode["fields"])

        self.popup = OpcodeSelector()
        self.popup.on_select(lambda code : on_select(code))
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
                    self.popup.on_select(lambda code : i.setText(code))
                    self.popup.show()
                inp.button.clicked.connect(lambda : open_popup())
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
            self.table_lines_list.addItem(entry)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TableManager()
    window.show()

    sys.exit(app.exec_())
