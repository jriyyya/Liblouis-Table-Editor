import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from components.Menubar import create_menubar
from components.TableEditor import TableEditor
from utils.ApplyStyles import apply_styles

class TableManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Liblouis Tables Manager')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        self.menubar = create_menubar(self)
        layout.setMenuBar(self.menubar)

        # Tab widget for file contents
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Make tabs closable
        self.tab_widget.tabCloseRequested.connect(self.close_tab)  # Connect close event

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        apply_styles(self)

        # Create an instance of TableEditor
        self.table_editor = TableEditor()

    def add_tab(self, file_name, file_content):
        new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the content in TableEditor
        self.table_editor.set_content(file_content)

        layout.addWidget(self.table_editor)
        new_tab.setLayout(layout)

        self.tab_widget.addTab(new_tab, file_name)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 248, 255))  # Light blue background
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 248, 255))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 248, 255))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(70, 130, 180))  # Steel blue highlight
    palette.setColor(QPalette.HighlightedText, Qt.white)

    app.setPalette(palette)

    window = TableManager()
    window.show()

    sys.exit(app.exec_())
