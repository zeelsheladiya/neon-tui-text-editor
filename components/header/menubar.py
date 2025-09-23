from textual.widgets import Static
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen


class EditMenuScreen(ModalScreen):
    """Edit menu dropdown screen"""
    
    def compose(self):
        with Vertical(classes="edit-menu-container"):
            yield Static("Undo          Ctrl+Z", classes="edit-menu-item", id="menu-undo")
            yield Static("Redo          Ctrl+U", classes="edit-menu-item", id="menu-redo")
            yield Static("─" * 25, classes="separator")  # Separator
            yield Static("Cut           Ctrl+X", classes="edit-menu-item", id="menu-cut")
            yield Static("Copy          Ctrl+C", classes="edit-menu-item", id="menu-copy")
            yield Static("Paste         Ctrl+V", classes="edit-menu-item", id="menu-paste")
            yield Static("─" * 25, classes="separator")  # Separator
            yield Static("Select All    Ctrl+A", classes="edit-menu-item", id="menu-select-all")
    
    def on_click(self, event):
        """Handle menu item clicks"""
        if hasattr(event.widget, 'id'):
            if event.widget.id == "menu-undo":
                self.app.action_undo()
            elif event.widget.id == "menu-redo":
                self.app.action_redo()
            elif event.widget.id == "menu-cut":
                self.app.action_cut()
            elif event.widget.id == "menu-copy":
                self.app.action_copy()
            elif event.widget.id == "menu-paste":
                self.app.action_paste()
            elif event.widget.id == "menu-select-all":
                self.app.action_select_all()
        
        # Close menu after selection
        self.dismiss()
    
    def on_key(self, event):
        """Close menu on Escape or any key"""
        self.dismiss()


class MenuBar(Static):
    """Menu bar component with File, Edit menus"""
    
    def compose(self):
        with Horizontal():
            yield Static("File", classes="menu-item", id="file-menu")
            yield Static("Edit", classes="menu-item", id="edit-menu")
            yield Static("Text Editor", classes="title")
    
    def on_click(self, event):
        """Handle menu clicks"""
        try:
            if hasattr(event.widget, 'id'):
                if event.widget.id == "file-menu":
                    self.app.notify("File menu - coming soon!", severity="info")
                elif event.widget.id == "edit-menu":
                    self.app.push_screen(EditMenuScreen())
        except Exception:
            pass