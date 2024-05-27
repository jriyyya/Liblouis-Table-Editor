from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.QtAsync import AsyncTask, coroutine
import json

data = json.load(open('./src/assets/data/opcodes.json', 'r'))
opcodes = data["codes"]

class OpcodeSelector(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWindowTitle('Opcode Selection Tool')

        layout = QVBoxLayout()

        search = QLineEdit()
        search.setPlaceholderText("Search for Opcode (hover for details)")

        label = QLabel("Double click opcode to select")

        self.list = QListWidget()
        self.list.itemClicked.connect(lambda x : search.setText(x.text()))

        layout.addWidget(search)
        layout.addWidget(label)
        layout.addWidget(self.list)

        self.populate_list()

        self.setLayout(layout)

    def populate_list(self):        
        for i, opcode in enumerate(opcodes):
            item = QListWidgetItem(f"{i}. {opcode["code"]}")
            item.setToolTip(opcode["description"])
            self.list.addItem(item)

    def on_select(self, cb):
        def callback(code):
            cb(code)
            self.hide()
        self.list.itemDoubleClicked.connect(lambda x : callback(opcodes[int(x.text().split('.')[0])]))