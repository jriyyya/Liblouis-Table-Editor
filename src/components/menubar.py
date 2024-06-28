from PyQt5.QtWidgets import QMenuBar, QAction
from PyQt5.QtGui import QIcon
import os

def create_action(parent, title, icon_path=None, shortcut=None):
    action = QAction(title, parent)
    if icon_path:
        action.setIcon(QIcon(icon_path))
    if shortcut:
        action.setShortcut(shortcut)
    return action

def add_menu_with_actions(menubar, title, actions):
    menu = menubar.addMenu(title)
    for action in actions:
        if action == 'separator':
            menu.addSeparator()
        else:
            menu.addAction(action)
    return menu

def create_menubar(parent):
    menubar = QMenuBar(parent)

    # Base path for icons
    icon_base_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icons')

    # Define menu structure with icon paths
    menu_structure = {
        'File': [
            ('New', os.path.join(icon_base_path, 'new.png'), 'Ctrl+N'),
            ('Open', os.path.join(icon_base_path, 'open.png'), 'Ctrl+O'),
            ('Save', os.path.join(icon_base_path, 'save.png'), 'Ctrl+S'),
            ('Save As', os.path.join(icon_base_path, 'save_as.png'), 'Ctrl+Shift+S')
        ],
        'Edit': [
            ('Undo', os.path.join(icon_base_path, 'undo.png'), 'Ctrl+Z'),
            ('Redo', os.path.join(icon_base_path, 'redo.png'), 'Ctrl+Y'),
            'separator',
            ('Go to Entry', os.path.join(icon_base_path, 'go_to_entry.png'), 'Ctrl+I'),
            ('Find', os.path.join(icon_base_path, 'find.png'), 'Ctrl+F'),
            ('Find and Replace', os.path.join(icon_base_path, 'find_replace.png'), 'Ctrl+H')
        ],
        'Tools': [
            ('Increase Font Size', os.path.join(icon_base_path, 'increase_font.png'), 'Ctrl+]'),
            ('Decrease Font Size', os.path.join(icon_base_path, 'decrease_font.png'), 'Ctrl+[')
        ],
        'Help': [
            ('About', os.path.join(icon_base_path, 'about.png'), None),
            ('Report a bug', os.path.join(icon_base_path, 'report_bug.png'), None),
            ('User Guide', os.path.join(icon_base_path, 'user_guide.png'), None)
        ]
    }

    # Add menus and actions
    for menu_title, actions in menu_structure.items():
        action_list = []
        for action in actions:
            if action == 'separator':
                action_list.append('separator')
            else:
                title, icon_path, shortcut = action
                action_list.append(create_action(parent, title, icon_path, shortcut))
        add_menu_with_actions(menubar, menu_title, action_list)

    return menubar
