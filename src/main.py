import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QFile, QTextStream  # Import QFile and QTextStream
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from components.Menubar import create_menubar
from components.TableEditor import TableEditor

class TableManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Liblouis Tables Manager')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Create menubar
        menubar = create_menubar(self)

        # Set the menubar
        layout.setMenuBar(menubar)

        # Tab widget for file contents
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Make tabs closable
        self.tab_widget.tabCloseRequested.connect(self.close_tab)  # Connect close event

        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

        self.apply_stylesheet("./src/styles.css")

    def add_tab(self, file_name, file_content):
        new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create an instance of TableEditor
        table_editor = TableEditor()
        table_editor.set_content(file_content)
        
        layout.addWidget(table_editor)
        new_tab.setLayout(layout)
        
        self.tab_widget.addTab(new_tab, file_name)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def apply_stylesheet(self, path):
        style_file = QFile(path)
        if not style_file.open(QFile.ReadOnly | QFile.Text):
            print(f"Failed to open stylesheet: {path}")
            return
        
        style_stream = QTextStream(style_file)
        style_sheet = style_stream.readAll()
        self.setStyleSheet(style_sheet)
        
        style_file.close()

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
