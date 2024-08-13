from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QMenu, QAction, QLineEdit
from PyQt5.QtCore import Qt

class EntryWidget(QWidget):
    def __init__(self, entry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.initUI()

    def initUI(self):
        self.label_text = QLabel(self.entry)
        self.label_text.setWordWrap(False)  # Ensure it displays on a single line

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label_text, alignment=Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing
        self.setLayout(self.layout)

        self.setStyleSheet("padding: 10px; background-color: white; margin: 0px")

        self.setMouseTracking(True)
        self.enterEvent = self.onHoverEnter
        self.leaveEvent = self.onHoverLeave

        self.edit_line = QLineEdit(self.entry)
        self.edit_line.setVisible(False)
        self.edit_line.setStyleSheet("background-color: #e0f7fa;")  # Edit mode background color
        self.layout.addWidget(self.edit_line)
        self.edit_line.editingFinished.connect(self.save_entry)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        duplicate_action = QAction('Duplicate', self)
        duplicate_action.triggered.connect(self.duplicate_entry)
        menu.addAction(duplicate_action)

        edit_action = QAction('Edit', self)
        edit_action.triggered.connect(self.edit_entry)
        menu.addAction(edit_action)

        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(self.delete_entry)
        menu.addAction(delete_action)

        menu.exec_(self.mapToGlobal(event.pos()))

    def duplicate_entry(self):
        new_entry_widget = EntryWidget(self.entry, parent=self.parentWidget())
        self.parentWidget().layout().insertWidget(self.parentWidget().layout().indexOf(self) + 1, new_entry_widget)

    def edit_entry(self):
        self.label_text.setVisible(False)
        self.edit_line.setVisible(True)
        self.edit_line.setText(self.entry)
        self.edit_line.setFocus()
        self.edit_line.selectAll()

    def save_entry(self):
        self.entry = self.edit_line.text()
        self.label_text.setText(self.entry)
        self.edit_line.setVisible(False)
        self.label_text.setVisible(True)

    def delete_entry(self):
        self.setParent(None)
        self.deleteLater()

    def onHoverEnter(self, event):
        self.setStyleSheet("padding: 10px; background-color: #f0f8ff; margin: 0px")

    def onHoverLeave(self, event):
        self.setStyleSheet("padding: 10px; background-color: white; margin: 0px")
