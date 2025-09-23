#!/usr/bin/env python3
"""
Text Editor - A VS Code-like text editor built with Textual
Usage: python editor.py [directory_path]
"""

import sys
import os
from pathlib import Path
from textual.app import App
from textual.containers import Vertical, Horizontal
from textual.widgets import Static
import subprocess
import platform

# Components
from components.header.menubar import MenuBar
from components.body.file_tree import FileTree
from components.body.editor_tabs import EditorTabs
from components.footer.status_bar import StatusBar


class TextEditor(App):
    """Main Text Editor Application"""
    
    CSS_PATH = [
        "styles/editor.tcss",
        "styles/header/menubar.tcss",
    ]
    
    def __init__(self, root_path: str = None):
        super().__init__()
        self.root_path = Path(root_path) if root_path else Path.cwd()
        
    def compose(self):
        """Create the application layout"""
        # Header - Menu bar
        yield MenuBar(id="menubar")
        
        # Body - Horizontal split
        with Horizontal(id="main-body"):
            # Left panel - File tree
            yield FileTree(self.root_path, id="file-tree")
            
            # Right panel - Editor with tabs
            yield EditorTabs(id="editor-tabs")
        
        # Footer - Status bar
        yield StatusBar(id="status-bar")
    
    def on_key(self, event):
        """Handle keyboard shortcuts"""
        if event.key == "ctrl+n":
            # New file - Control+N
            editor_tabs = self.query_one("#editor-tabs")
            editor_tabs.create_new_file()
            event.prevent_default()
        elif event.key == "ctrl+w":
            # Close current tab - Control+W
            editor_tabs = self.query_one("#editor-tabs")
            editor_tabs.close_current_tab()
            event.prevent_default()
        elif event.key == "ctrl+s":
            # Save current file - Control+S (placeholder)
            self.notify("Save functionality coming soon!", severity="info")
            event.prevent_default()
        elif event.key == "ctrl+j":
            # Navigate to previous tab - Control+J
            editor_tabs = self.query_one("#editor-tabs")
            editor_tabs.navigate_tab(-1)
            event.prevent_default()
        elif event.key == "ctrl+l":
            # Navigate to next tab - Control+L
            editor_tabs = self.query_one("#editor-tabs")
            editor_tabs.navigate_tab(1)
            event.prevent_default()
        elif event.key == "ctrl+z":
            # Undo - Control+Z
            try:
                editor = self.query_one("#editor-area")
                if hasattr(editor, 'undo'):
                    editor.undo()
                else:
                    self.notify("Undo not available", severity="warning")
            except Exception:
                self.notify("Undo failed", severity="error")
            event.prevent_default()
        elif event.key == "ctrl+u":
            # Redo - Control+U
            try:
                editor = self.query_one("#editor-area")
                if hasattr(editor, 'redo'):
                    editor.redo()
                else:
                    self.notify("Redo not available", severity="warning")
            except Exception:
                self.notify("Redo failed", severity="error")
            event.prevent_default()
        elif event.key == "ctrl+x":
            # Cut - Control+X
            self.action_cut()
            event.prevent_default()
        elif event.key == "ctrl+c":
            # Copy - Control+C
            self.action_copy()
            event.prevent_default()
        elif event.key == "ctrl+v":
            # Paste - Control+V
            self.action_paste()
            event.prevent_default()
        elif event.key == "ctrl+a":
            # Select All - Control+A
            self.action_select_all()
            event.prevent_default()
    
    def action_undo(self):
        """Undo action"""
        try:
            editor = self.query_one("#editor-area")
            if hasattr(editor, 'undo'):
                editor.undo()
                self.notify("Undo", severity="info")
            else:
                self.notify("Undo not available", severity="warning")
        except Exception:
            self.notify("Undo failed", severity="error")
    
    def action_redo(self):
        """Redo action"""
        try:
            editor = self.query_one("#editor-area")
            if hasattr(editor, 'redo'):
                editor.redo()
                self.notify("Redo", severity="info")
            else:
                self.notify("Redo not available", severity="warning")
        except Exception:
            self.notify("Redo failed", severity="error")
    
    def get_clipboard_text(self):
        """Get text from system clipboard"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                return result.stdout
            elif system == "Linux":
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True)
                return result.stdout
            elif system == "Windows":
                result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], capture_output=True, text=True)
                return result.stdout
            else:
                return ""
        except Exception:
            return ""
    
    def set_clipboard_text(self, text):
        """Set text to system clipboard"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(['pbcopy'], input=text, text=True)
                return True
            elif system == "Linux":
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text, text=True)
                return True
            elif system == "Windows":
                subprocess.run(['powershell', '-command', f'Set-Clipboard -Value "{text}"'], text=True)
                return True
            else:
                return False
        except Exception:
            return False
    
    def action_cut(self):
        """Cut action"""
        try:
            editor = self.query_one("#editor-area")
            
            # First copy the text
            self.action_copy()
            
            # Then delete the selected text or current line
            if hasattr(editor, 'selection') and not editor.selection.is_empty:
                # Delete selected text by replacing with empty string
                try:
                    # Get selection bounds
                    start = editor.selection.start
                    end = editor.selection.end
                    
                    # Replace selection with empty string
                    editor.replace("", start, end)
                    self.notify("Cut to clipboard", severity="info")
                except Exception:
                    self.notify("Cut completed (copy successful, delete failed)", severity="warning")
            else:
                # For line cutting, just notify that copy was successful
                self.notify("Line copied to clipboard (line cut not fully supported)", severity="info")
                    
        except Exception as e:
            self.notify(f"Cut failed: {e}", severity="error")
    
    def action_copy(self):
        """Copy action"""
        try:
            editor = self.query_one("#editor-area")
            
            # Check if there's selected text
            if hasattr(editor, 'selection') and not editor.selection.is_empty:
                # Get selected text
                selected_text = editor.selected_text
                
                # Copy to clipboard
                if self.set_clipboard_text(selected_text):
                    self.notify("Copied to clipboard", severity="info")
                else:
                    self.notify("Failed to access clipboard", severity="error")
            else:
                # If no selection, copy current line
                cursor_line = editor.cursor_location[0]
                line_text = editor.document.get_line(cursor_line)
                
                if self.set_clipboard_text(line_text):
                    self.notify("Copied line to clipboard", severity="info")
                else:
                    self.notify("Failed to access clipboard", severity="error")
                    
        except Exception as e:
            self.notify(f"Copy failed: {e}", severity="error")
    
    def action_paste(self):
        """Paste action"""
        try:
            editor = self.query_one("#editor-area")
            
            # Get text from clipboard
            clipboard_text = self.get_clipboard_text()
            
            if clipboard_text:
                # Insert text at cursor position
                cursor_location = editor.cursor_location
                editor.insert(clipboard_text, cursor_location)
                self.notify("Pasted from clipboard", severity="info")
            else:
                self.notify("Clipboard is empty", severity="warning")
                
        except Exception as e:
            self.notify(f"Paste failed: {e}", severity="error")
    
    def action_select_all(self):
        """Select all action"""
        try:
            editor = self.query_one("#editor-area")
            
            # Select all text in the document
            if hasattr(editor, 'select_all'):
                editor.select_all()
                self.notify("Selected all text", severity="info")
            else:
                # Manual selection if select_all not available
                start = (0, 0)
                end_line = len(editor.document.lines) - 1
                end_col = len(editor.document.get_line(end_line))
                end = (end_line, end_col)
                
                editor.selection = editor.selection.update(start, end)
                self.notify("Selected all text", severity="info")
                
        except Exception as e:
            self.notify(f"Select all failed: {e}", severity="error")


def main():
    """Entry point with command line argument support"""
    root_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if root_path and not os.path.exists(root_path):
        print(f"Error: Directory '{root_path}' does not exist")
        sys.exit(1)
        
    app = TextEditor(root_path)
    app.run()


if __name__ == "__main__":
    main() 