from pathlib import Path
from textual.widgets import Static, TextArea, TabbedContent, TabPane
from textual.containers import Vertical, Horizontal
from textual.reactive import reactive


class EditorTabs(Static):
    """Editor with tabs component - like VS Code"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open_files = {}  # Track open files
        self.untitled_count = 0
        self.current_tab = None  # Track current active tab
        
    def compose(self):
        with Vertical():
            # Tab bar with + button
            with Horizontal(classes="tab-bar"):
                yield Static("Welcome", classes="tab active", id="welcome-tab")
                yield Static("+", classes="new-tab-btn", id="new-tab-btn")
            
            # Editor area
            yield TextArea("Welcome to Text Editor!\n\nPress Ctrl+N for new file or select a file from the tree.", 
                          id="editor-area", classes="editor", show_line_numbers=True)
    
    def on_click(self, event):
        """Handle tab and button clicks"""
        if event.widget.id == "new-tab-btn":
            self.create_new_file()
        elif "tab" in event.widget.classes:
            self.switch_to_tab(event.widget)
        
        # Update status bar after any click
        self.call_after_refresh(self.update_status_bar)
    
    def on_text_area_changed(self, event):
        """Handle text area changes"""
        self.call_after_refresh(self.update_status_bar)
    
    def on_key(self, event):
        """Handle key presses to update cursor position"""
        self.call_after_refresh(self.update_status_bar)
    
    def close_current_tab(self):
        """Close the currently active tab"""
        try:
            # Find the active tab
            active_tab = None
            for tab in self.query(".tab"):
                if "active" in tab.classes:
                    active_tab = tab
                    break
            
            if not active_tab or active_tab.id == "welcome-tab":
                # Don't close welcome tab, just clear editor
                editor = self.query_one("#editor-area")
                editor.text = "Welcome to Text Editor!\n\nPress Ctrl+N for new file or select a file from the tree."
                self.current_tab = None
                self.app.notify("Welcome tab cleared", severity="info")
                return
            
            # Get safe_id from tab ID
            safe_id = active_tab.id.replace("tab-", "")
            
            # Find filename by safe_id
            filename_to_close = None
            for filename, file_info in self.open_files.items():
                if file_info.get("safe_id") == safe_id:
                    filename_to_close = filename
                    break
            
            if filename_to_close:
                # Remove from open files
                del self.open_files[filename_to_close]
                self.app.notify(f"Closed {filename_to_close}", severity="info")
            
            # Remove tab from UI
            active_tab.remove()
            
            # Switch to welcome tab if no other tabs
            if not self.open_files:
                welcome_tab = self.query_one("#welcome-tab")
                self.switch_to_tab(welcome_tab)
                editor = self.query_one("#editor-area")
                editor.text = "Welcome to Text Editor!\n\nPress Ctrl+N for new file or select a file from the tree."
            else:
                # Switch to the first available tab
                first_tab = self.query(".tab").first()
                if first_tab:
                    self.switch_to_tab(first_tab)
                
        except Exception as e:
            self.app.notify(f"Error closing tab: {e}", severity="error")
    
    def navigate_tab(self, direction: int):
        """Navigate between tabs using arrow keys"""
        try:
            # Get all tabs
            all_tabs = list(self.query(".tab"))
            if len(all_tabs) <= 1:
                return  # No navigation needed with 0 or 1 tabs
            
            # Find current active tab
            current_index = 0
            for i, tab in enumerate(all_tabs):
                if "active" in tab.classes:
                    current_index = i
                    break
            
            # Calculate new index with wrapping
            new_index = (current_index + direction) % len(all_tabs)
            
            # Switch to new tab
            new_tab = all_tabs[new_index]
            self.switch_to_tab(new_tab)
            
            # Scroll tab into view if needed
            self.scroll_tab_into_view(new_tab)
            
        except Exception as e:
            pass
    
    def scroll_tab_into_view(self, tab_widget):
        """Scroll the tab bar to make the specified tab visible"""
        try:
            tab_bar = self.query_one(".tab-bar")
            
            # Get the tab's position and the tab bar's viewport
            tab_region = tab_widget.region
            tab_bar_region = tab_bar.region
            
            # Calculate if tab is outside visible area
            tab_left = tab_region.x
            tab_right = tab_region.x + tab_region.width
            viewport_left = tab_bar.scroll_x
            viewport_right = tab_bar.scroll_x + tab_bar_region.width
            
            # Scroll if tab is outside viewport
            if tab_left < viewport_left:
                # Tab is to the left of viewport, scroll left
                tab_bar.scroll_x = max(0, tab_left - 2)
            elif tab_right > viewport_right:
                # Tab is to the right of viewport, scroll right
                tab_bar.scroll_x = tab_right - tab_bar_region.width + 2
                
        except Exception as e:
            # Fallback: try simpler scroll method
            try:
                tab_bar = self.query_one(".tab-bar")
                tab_bar.scroll_to_widget(tab_widget, animate=False)
            except Exception:
                pass
    
    def create_new_file(self):
        """Create a new untitled file"""
        self.untitled_count += 1
        filename = f"Untitled-{self.untitled_count}"
        
        # Add new tab
        tab_bar = self.query_one(".tab-bar")
        new_tab_btn = self.query_one("#new-tab-btn")
        
        # Create safe ID (replace invalid characters)
        safe_id = filename.replace(".", "-").replace(" ", "-")
        
        # Create simple tab
        new_tab = Static(f"{filename} *", classes="tab", id=f"tab-{safe_id}")
        tab_bar.mount(new_tab, before=new_tab_btn)
        
        # Switch to new tab
        self.switch_to_tab(new_tab)
        
        # Store file info
        self.open_files[filename] = {
            "path": None,
            "content": "",
            "modified": True,
            "safe_id": safe_id
        }
    
    def open_file(self, file_path: Path):
        """Open a file in a new tab"""
        filename = file_path.name
        
        # Check if file is already open
        if filename in self.open_files:
            # Switch to existing tab
            try:
                safe_id = self.open_files[filename]["safe_id"]
                existing_tab = self.query_one(f"#tab-{safe_id}")
                self.switch_to_tab(existing_tab)
                return
            except:
                pass
        
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8')
            
            # Add new tab
            tab_bar = self.query_one(".tab-bar")
            new_tab_btn = self.query_one("#new-tab-btn")
            
            # Create safe ID (replace invalid characters)
            safe_id = filename.replace(".", "-").replace(" ", "-").replace("_", "-")
            
            # Create simple tab
            new_tab = Static(filename, classes="tab", id=f"tab-{safe_id}")
            tab_bar.mount(new_tab, before=new_tab_btn)
            
            # Switch to new tab and load content
            self.switch_to_tab(new_tab)
            editor = self.query_one("#editor-area")
            editor.text = content
            
            # Store file info
            self.open_files[filename] = {
                "path": file_path,
                "content": content,
                "modified": False,
                "safe_id": safe_id
            }
            
            # Update status bar
            self.call_after_refresh(self.update_status_bar)
            
        except Exception as e:
            # Handle file read errors
            self.app.notify(f"Error opening file: {e}", severity="error")
    
    def switch_to_tab(self, tab_widget):
        """Switch to the selected tab"""
        try:
            # Save current tab content before switching
            self.save_current_tab_content()
            
            # Remove active class from all tabs
            for tab in self.query(".tab"):
                tab.remove_class("active")
            
            # Add active class to selected tab
            tab_widget.add_class("active")
            
            # Get safe_id from tab ID
            tab_id = tab_widget.id
            if tab_id == "welcome-tab":
                editor = self.query_one("#editor-area")
                editor.text = "Welcome to Text Editor!\n\nPress Ctrl+N for new file or select a file from the tree."
                self.current_tab = None
                return
                
            safe_id = tab_id.replace("tab-", "")
            
            # Find filename by safe_id
            for filename, file_info in self.open_files.items():
                if file_info.get("safe_id") == safe_id:
                    editor = self.query_one("#editor-area")
                    editor.text = file_info["content"]
                    self.current_tab = filename
                    
                    # Update status bar
                    self.call_after_refresh(self.update_status_bar)
                    break
                    
        except Exception as e:
            # Handle any errors gracefully
            pass
    
    def save_current_tab_content(self):
        """Save the current editor content to the active tab"""
        try:
            if hasattr(self, 'current_tab') and self.current_tab and self.current_tab in self.open_files:
                editor = self.query_one("#editor-area")
                self.open_files[self.current_tab]["content"] = editor.text
        except Exception:
            pass
    
    def on_mount(self):
        """Set up cursor tracking when component mounts"""
        try:
            editor = self.query_one("#editor-area")
            editor.cursor_blink = True
            # Set up periodic status bar updates
            self.set_interval(0.1, self.update_status_bar)
        except Exception:
            pass
    
    def update_status_bar(self):
        """Update status bar with current file info and cursor position"""
        try:
            editor = self.query_one("#editor-area")
            status_bar = self.app.query_one("#status-bar")
            
            # Get cursor position using different methods
            cursor_line = 1
            cursor_col = 1
            
            try:
                # Try cursor_location first
                if hasattr(editor, 'cursor_location'):
                    cursor_line = editor.cursor_location[0] + 1
                    cursor_col = editor.cursor_location[1] + 1
                elif hasattr(editor, 'cursor_row') and hasattr(editor, 'cursor_column'):
                    cursor_line = editor.cursor_row + 1
                    cursor_col = editor.cursor_column + 1
                elif hasattr(editor, 'selection'):
                    cursor_line = editor.selection.end[0] + 1
                    cursor_col = editor.selection.end[1] + 1
            except Exception:
                # Use fallback values
                pass
            
            # Update line/column
            status_bar.update_line_col(cursor_line, cursor_col)
            
            # Update file info if we have a current tab
            if hasattr(self, 'current_tab') and self.current_tab and self.current_tab in self.open_files:
                file_info = self.open_files[self.current_tab]
                status_bar.update_current_file(self.current_tab)
                
                if file_info["path"]:
                    file_ext = file_info["path"].suffix or "Plain Text"
                    status_bar.update_file_type(file_ext)
                else:
                    status_bar.update_file_type("Plain Text")
            else:
                status_bar.update_current_file("Welcome")
                status_bar.update_file_type("Plain Text")
                
        except Exception as e:
            # Debug: show what went wrong
            pass