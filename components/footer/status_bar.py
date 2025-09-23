from textual.widgets import Static
from textual.containers import Horizontal


class StatusBar(Static):
    """Status bar component showing file info and editor status"""
    
    def compose(self):
        with Horizontal():
            yield Static("Welcome", id="current-file")
            yield Static("Ln 1, Col 1", id="line-col")
            yield Static("Plain Text", id="file-type")
    
    def update_current_file(self, filename: str):
        """Update current file display"""
        try:
            file_widget = self.query_one("#current-file")
            file_widget.update(filename)
        except:
            pass
    
    def update_line_col(self, line: int, col: int):
        """Update line/column position"""
        try:
            pos_widget = self.query_one("#line-col")
            pos_widget.update(f"Ln {line}, Col {col}")
        except:
            pass
    
    def update_file_type(self, file_type: str):
        """Update file type display"""
        try:
            type_widget = self.query_one("#file-type")
            type_widget.update(file_type)
        except:
            pass