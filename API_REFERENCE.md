# API Reference

## 📚 Component API Documentation

### TextEditor (Main Application)

**File**: `editor.py`

#### Constructor
```python
TextEditor(root_path: str = None)
```
- `root_path`: Optional directory path to open (defaults to current directory)

#### Methods
```python
def compose(self) -> ComposeResult
    """Create the application layout"""

def on_key(self, event: Key) -> None
    """Handle global keyboard shortcuts"""

def action_undo(self) -> None
    """Undo last action"""

def action_redo(self) -> None
    """Redo last undone action"""

def action_cut(self) -> None
    """Cut selected text to clipboard"""

def action_copy(self) -> None
    """Copy selected text to clipboard"""

def action_paste(self) -> None
    """Paste text from clipboard"""

def action_select_all(self) -> None
    """Select all text in editor"""

def get_clipboard_text(self) -> str
    """Get text from system clipboard"""

def set_clipboard_text(self, text: str) -> bool
    """Set text to system clipboard"""

def resize_file_tree(self, change: int) -> None
    """Resize the file tree panel by specified percentage"""
```

#### Layout Management
- **Resizable Panels**: File tree width adjustable from 15% to 80%
- **State Tracking**: Width tracked in `self.file_tree_width` variable
- **Responsive Editor**: Editor tabs automatically adjust to remaining space

#### Keyboard Shortcuts
- `Control+N`: Create new file
- `Control+W`: Close current tab  
- `Control+S`: Save file (placeholder)
- `Control+J`: Navigate to previous tab
- `Control+L`: Navigate to next tab
- `Control+Z`: Undo last action
- `Control+U`: Redo last undone action
- `Control+X`: Cut selected text to clipboard
- `Control+C`: Copy selected text to clipboard
- `Control+V`: Paste text from clipboard
- `Control+A`: Select all text in editor
- `Control+Shift+Left`: Decrease file tree width
- `Control+Shift+Right`: Increase file tree width

---

### MenuBar Component

**File**: `components/header/menubar.py`

#### Class
```python
class MenuBar(Static)
```

#### Methods
```python
def compose(self) -> ComposeResult
    """Create menu bar layout with File, Edit, and title"""

def on_click(self, event: Click) -> None
    """Handle menu item clicks"""
```

#### Edit Menu Features
- **Modal Screen**: Edit menu opens as modal with all options
- **Text Operations**: Undo, Redo, Cut, Copy, Paste, Select All
- **Keyboard Shortcuts**: Shows shortcuts next to each option
- **Auto-close**: Menu closes after selection or key press

#### Events
- Click on "File" menu item (placeholder)
- Click on "Edit" menu item (opens EditMenuScreen)
- Hover effects via CSS

---

### FileTree Component

**File**: `components/body/file_tree.py`

#### Class
```python
class FileTree(Tree)
```

#### Constructor
```python
FileTree(root_path: Path, **kwargs)
```
- `root_path`: Directory path to display

#### Methods
```python
def on_mount(self) -> None
    """Initialize file tree when mounted"""

def load_directory(self, path: Path, node: TreeNode) -> None
    """Load directory contents into tree node"""

def get_file_icon(self, file_path: Path) -> str
    """Get appropriate icon for file based on extension"""

def on_tree_node_expanded(self, event: TreeNodeExpanded) -> None
    """Handle directory expansion"""

def on_tree_node_selected(self, event: TreeNodeSelected) -> None
    """Handle file/directory selection"""
```

#### Node Data Structure
```python
node.data = {
    "path": Path,           # File/directory path
    "type": str            # "file", "directory", "error", "placeholder"
}
```

#### Events
- `TreeNodeExpanded`: Directory expanded
- `TreeNodeSelected`: File/directory clicked

---

### EditorTabs Component

**File**: `components/body/editor_tabs.py`

#### Class
```python
class EditorTabs(Static)
```

#### Attributes
```python
self.open_files: Dict[str, FileInfo]  # Tracking open files
self.untitled_count: int              # Counter for new files
self.current_tab: str                 # Currently active tab
```

#### FileInfo Structure
```python
{
    "path": Path | None,    # File path (None for untitled)
    "content": str,         # File content
    "modified": bool,       # Modification status
    "safe_id": str         # HTML-safe ID
}
```

#### Methods

##### File Operations
```python
def create_new_file(self) -> None
    """Create new untitled file"""

def open_file(self, file_path: Path) -> None
    """Open file from filesystem"""
    
def close_current_tab(self) -> None
    """Close currently active tab"""

def navigate_tab(self, direction: int) -> None
    """Navigate between tabs using keyboard shortcuts"""

def scroll_tab_into_view(self, tab_widget: Widget) -> None
    """Scroll tab bar to make specified tab visible"""
```

##### Tab Management
```python
def switch_to_tab(self, tab_widget: Widget) -> None
    """Switch to specified tab"""

def save_current_tab_content(self) -> None
    """Save current editor content to tab data"""
```

##### Status Updates
```python
def update_status_bar(self) -> None
    """Update status bar with current file info"""

def on_mount(self) -> None
    """Set up periodic status updates"""
```

#### Events
```python
def on_click(self, event: Click) -> None
    """Handle tab and button clicks"""

def on_text_area_changed(self, event: TextAreaChanged) -> None
    """Handle text changes"""

def on_key(self, event: Key) -> None
    """Handle key presses for cursor tracking"""
```

#### Safe ID System
Converts filenames to valid HTML IDs:
```python
safe_id = filename.replace(".", "-").replace(" ", "-").replace("_", "-")
```

---

### StatusBar Component

**File**: `components/footer/status_bar.py`

#### Class
```python
class StatusBar(Static)
```

#### Methods
```python
def compose(self) -> ComposeResult
    """Create status bar layout"""

def update_current_file(self, filename: str) -> None
    """Update current file display"""

def update_line_col(self, line: int, col: int) -> None
    """Update cursor position display"""

def update_file_type(self, file_type: str) -> None
    """Update file type display"""
```

#### Layout Structure
```
StatusBar (Horizontal)
├── #current-file (1fr width, orange text)
├── #line-col (20 chars, centered)
└── #file-type (20 chars, right-aligned)
```

---

## 🎨 CSS Classes and IDs

### Main Layout
```css
#menubar          /* Menu bar container */
#main-body        /* Horizontal body container */
#file-tree        /* File tree container */
#editor-tabs      /* Editor tabs container */
#status-bar       /* Status bar container */
```

### MenuBar
```css
.menu-item        /* File/Edit menu items */
.title            /* Application title */
```

### FileTree
```css
FileTree          /* File tree component */
Tree              /* Tree widget styling */
Tree:focus        /* Focused tree styling */
```

### EditorTabs
```css
.tab-bar          /* Tab bar container */
.tab              /* Individual tab */
.tab:hover        /* Tab hover state */
.tab.active       /* Active tab */
.new-tab-btn      /* New tab (+) button */
#editor-area      /* Text editor area */
```

### StatusBar
```css
#current-file     /* Current filename display */
#line-col         /* Line/column position */
#file-type        /* File type display */
```

---

## 🔧 Utility Functions

### Safe ID Generation
```python
def generate_safe_id(filename: str) -> str:
    """Convert filename to HTML-safe ID"""
    return filename.replace(".", "-").replace(" ", "-").replace("_", "-")
```

### File Type Detection
```python
def get_file_type(file_path: Path) -> str:
    """Get file type from extension"""
    return file_path.suffix or "Plain Text"
```

### Content Persistence
```python
def save_tab_content(tab_name: str, content: str) -> None:
    """Save tab content to memory"""
    
def load_tab_content(tab_name: str) -> str:
    """Load tab content from memory"""
```

---

## 📡 Event System

### Global Events (TextEditor)
```python
Key("ctrl+n")     # New file
Key("ctrl+w")     # Close tab
Key("ctrl+s")     # Save file
Key("ctrl+j")     # Previous tab
Key("ctrl+l")     # Next tab
Key("ctrl+z")     # Undo
Key("ctrl+u")     # Redo
Key("ctrl+x")     # Cut
Key("ctrl+c")     # Copy
Key("ctrl+v")     # Paste
Key("ctrl+a")     # Select all
Key("ctrl+shift+left")   # Decrease file tree width
Key("ctrl+shift+right")  # Increase file tree width
```

### Component Events

#### FileTree Events
```python
TreeNodeExpanded  # Directory expanded
TreeNodeSelected  # File/directory selected
```

#### EditorTabs Events
```python
Click             # Tab or button clicked
TextAreaChanged   # Editor content changed
Key               # Key pressed in editor
```

#### MenuBar Events
```python
Click             # Menu item clicked
```

---

## 🗂️ Data Structures

### Application State
```python
{
    "root_path": Path,              # Working directory
    "components": {                 # Component references
        "menubar": MenuBar,
        "file_tree": FileTree,
        "editor_tabs": EditorTabs,
        "status_bar": StatusBar
    }
}
```

### File Management
```python
open_files = {
    "filename.py": {
        "path": Path("/path/to/filename.py"),
        "content": "file content string",
        "modified": False,
        "safe_id": "filename-py"
    }
}
```

### Tree Node Data
```python
node.data = {
    "path": Path("/path/to/item"),
    "type": "file" | "directory" | "error" | "placeholder"
}
```

---

## 🎯 Extension Points

### Adding New Components
1. Inherit from appropriate Textual widget
2. Implement `compose()` method
3. Add event handlers as needed
4. Register in main app layout
5. Add CSS styling

### Adding New Events
1. Define custom event class
2. Post event with `self.post_message()`
3. Handle with `on_custom_event()` method

### Adding New Shortcuts
1. Add to `TextEditor.on_key()` method
2. Implement handler method
3. Call `event.prevent_default()`

### Adding New Menus
1. Add menu item to MenuBar
2. Implement click handler
3. Add dropdown logic (future)

---

## 🔍 Query Selectors

### Component Access
```python
# By ID
menubar = self.query_one("#menubar")
editor = self.query_one("#editor-area")

# By class
tabs = self.query(".tab")
menu_items = self.query(".menu-item")

# By type
all_statics = self.query(Static)
```

### Common Queries
```python
# Get active tab
active_tab = self.query_one(".tab.active")

# Get all tabs
all_tabs = self.query(".tab")

# Get editor area
editor = self.query_one("#editor-area")

# Get status bar components
current_file = self.query_one("#current-file")
line_col = self.query_one("#line-col")
file_type = self.query_one("#file-type")
```

---

This API reference provides the essential information needed to understand and extend the text editor codebase.