class Main:

    def __init__(self, ui):
        self.ui = ui

    def toggle_edit_mode(self):
        self.ui.state['edit'] = not self.ui.state['edit']
        self.ui.state['deselect'] = True

    def center(self):
        self.ui.state['scroll_x'] = 0
        self.ui.state['scroll_y'] = 0
        self.ui.state['scale'] = 1

    def add_text(self):
        self.ui.add['text'] = True
