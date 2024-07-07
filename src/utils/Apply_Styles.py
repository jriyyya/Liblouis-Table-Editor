# style_utils.py

from PyQt5.QtCore import QFile, QTextStream

def apply_styles(widget):
    
    stylesheet_path = "./src/styles.css"
    style_file = QFile(stylesheet_path)
    if not style_file.open(QFile.ReadOnly | QFile.Text):
        print(f"Failed to open stylesheet: {stylesheet_path}")
        return False
    
    style_stream = QTextStream(style_file)
    style_sheet = style_stream.readAll()
    widget.setStyleSheet(style_sheet)
    
    style_file.close()
    return True
