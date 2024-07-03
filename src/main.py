# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
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

        self.apply_styles()

    def add_tab(self, file_name, file_content):
        new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for each tab

        # Create an instance of TableEditor
        table_editor = TableEditor()
        table_editor.set_content(file_content)
        
        layout.addWidget(table_editor)
        new_tab.setLayout(layout)
        
        self.tab_widget.addTab(new_tab, file_name)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 16px;  /* Larger font size */
            }
            QTabWidget::pane {
                background: #F0F8FF;
            }
            QTabBar::tab {
                background: #1082B9;
                padding: 8px 10px;  /* Reduced vertical padding */
                min-width: 100px;
                font-weight: bold;
                color: black;  /* Text color */
            }
            QTabBar::tab:selected {
                background: #D4E9F7;  /* Light shade of blue */
                border-bottom-color: #D4E9F7;
            }
            QTabBar::tab:hover {
                background: #D4E9F7;  /* Light shade of blue */
            }
            QMenuBar {
                background: #F0F8FF;
            }
            QMenuBar::item {
                background: transparent;
                padding: 5px 15px;
                color: black;  /* Text color */
            }
            QMenuBar::item:selected {
                background: #D4E9F7;  /* Light shade of blue */
                color: black;  /* Ensure text color remains black */
            }
            QMenu {
                background: #F0F8FF;
            }
            QMenu::item {
                color: black;  /* Ensure text color remains black */
            }
            QMenu::item:selected {
                background: #D4E9F7;  /* Light shade of blue */
                color: black;  /* Ensure text color remains black */
            }
            QTextEdit {
                background: #FFFFFF;
                padding: 10px;
                color: black;  /* Text color */
            }
        """)


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
