import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from components.menubar import create_menubar

class TableManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Liblouis Tables Manager')
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        layout = QVBoxLayout()

        # Create menubar
        menubar = create_menubar(self)

        # Set the menubar
        layout.setMenuBar(menubar)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = TableManager()
    window.show()

    sys.exit(app.exec_())
