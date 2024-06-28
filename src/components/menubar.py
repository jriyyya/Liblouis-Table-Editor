from PyQt5.QtWidgets import QMenuBar, QAction

def create_action(parent, title, shortcut=None):
    action = QAction(title, parent)
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

    # Define menu structure
    menu_structure = {
        'File': [
            ('New', 'Ctrl+N'),
            ('Open', 'Ctrl+O'),
            ('Save', 'Ctrl+S'),
            ('Save As', 'Ctrl+Shift+S')
        ],
        'Edit': [
            ('Undo', 'Ctrl+Z'),
            ('Redo', 'Ctrl+Y'),
            'separator',
            ('Go to Entry', 'Ctrl+I'),
            ('Find', 'Ctrl+F'),
            ('Find and Replace', 'Ctrl+H')
        ],
        'Tools': [
            ('Increase Font Size', 'Ctrl+]'),
            ('Decrease Font Size', 'Ctrl+[')
        ],
        'Help': [
            ('About', None),
            ('Report a bug', None),
            ('User Guide', None)
        ]
    }

    # Add menus and actions
    for menu_title, actions in menu_structure.items():
        action_list = []
        for action in actions:
            if action == 'separator':
                action_list.append('separator')
            else:
                title, shortcut = action
                action_list.append(create_action(parent, title, shortcut))
        add_menu_with_actions(menubar, menu_title, action_list)

    return menubar
