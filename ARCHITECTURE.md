# Technical Architecture Documentation

## 🏛️ System Architecture

### High-Level Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    TextEditor (Main App)                    │
│  - Entry point & CLI argument handling                      │
│  - Global keyboard shortcuts                                │
│  - CSS styling system                                       │
│  - Component orchestration                                  │
└─────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │   MenuBar    │ │ Main Body │ │ StatusBar   │
        │   (Header)   │ │           │ │  (Footer)   │
        └──────────────┘ └─────┬─────┘ └─────────────┘
                               │
                    ┌──────────┼──────────┐
                    │                     │
            ┌───────▼──────┐    ┌────────▼────────┐
            │   FileTree   │    │   EditorTabs    │
            │ (Directory)  │    │   (Editor)      │
            └──────────────┘    └─────────────────┘
```

## 🧩 Component Deep Dive

### 1. TextEditor (Main Application)

**File**: `editor.py`
**Responsibilities**:
- Application lifecycle management
- Command-line argument processing
- Global event handling
- CSS style definitions
- Component layout orchestration

**Key Methods**:
```python
def __init__(self, root_path: str = None)
    # Initialize with optional directory path

def compose(self) -> ComposeResult
    # Define application layout structure

def on_key(self, event: Key) -> None
    # Handle global keyboard shortcuts
```

**CSS Architecture**:
- Inline CSS for maintainability
- Component-specific sections
- Neon color scheme with rounded borders
- Responsive layout properties

### 2. MenuBar Component

**File**: `components/header/menubar.py`
**Purpose**: Top navigation bar with expandable menu system

**Structure**:
```python
class MenuBar(Static):
    def compose(self):
        with Horizontal():
            yield Static("File", classes="menu-item", id="file-menu")
            yield Static("Edit", classes="menu-item", id="edit-menu")  
            yield Static("Text Editor", classes="title")
```

**Event Handling**:
- Click detection for menu items
- Hover effects via CSS
- Extensible for dropdown menus

**Future Extensions**:
- Dropdown menu implementation
- Context-sensitive menu items
- Keyboard navigation

### 3. FileTree Component

**File**: `components/body/file_tree.py`
**Purpose**: Directory browser with lazy loading

**Inheritance**: `Tree` (Textual widget)

**Key Features**:
- **Lazy Loading**: Directories loaded on expansion
- **File Type Detection**: Icons for files/folders
- **Permission Handling**: Graceful error handling
- **Click-to-Open**: Integration with editor tabs

**Data Structure**:
```python
# Node data format
node.data = {
    "path": Path("/path/to/file"),
    "type": "file" | "directory" | "error" | "placeholder"
}
```

**Event Handlers**:
```python
def on_tree_node_expanded(self, event)
    # Load directory contents on expansion

def on_tree_node_selected(self, event)
    # Open files in editor tabs
```

### 4. EditorTabs Component

**File**: `components/body/editor_tabs.py`
**Purpose**: Multi-tab text editor with content management

**Structure**:
```
EditorTabs (Static)
├── Tab Bar (Horizontal)
│   ├── Tab 1 (Static)
│   ├── Tab 2 (Static)
│   └── New Tab Button (+)
└── TextArea (Editor)
```

**State Management**:
```python
self.open_files = {
    "filename": {
        "path": Path,
        "content": str,
        "modified": bool,
        "safe_id": str
    }
}
self.current_tab = str  # Currently active tab
self.untitled_count = int  # Counter for new files
```

**Key Methods**:

#### File Operations
```python
def create_new_file(self) -> None
    # Creates new untitled file with unique name
    # Generates safe ID for HTML compatibility
    # Adds tab to UI and switches to it

def open_file(self, file_path: Path) -> None
    # Opens file from filesystem
    # Handles encoding and error cases
    # Creates tab and loads content
    # Updates status bar
```

#### Tab Management
```python
def switch_to_tab(self, tab_widget) -> None
    # Saves current tab content before switching
    # Updates active tab styling
    # Loads new tab content
    # Updates status bar with file info

def close_current_tab(self) -> None
    # Closes currently active tab
    # Handles welcome tab specially
    # Switches to remaining tab or welcome
```

#### Content Persistence
```python
def save_current_tab_content(self) -> None
    # Saves editor content to tab's data structure
    # Called before tab switches
    # Prevents content loss
```

**Safe ID System**:
Converts filenames to valid HTML IDs:
```python
safe_id = filename.replace(".", "-").replace(" ", "-").replace("_", "-")
# "my file.py" → "my-file-py"
```

### 5. StatusBar Component

**File**: `components/footer/status_bar.py`
**Purpose**: Real-time status information display

**Layout**:
```
StatusBar (Horizontal)
├── Current File (1fr width, orange)
├── Line/Column (20 chars, center)
└── File Type (20 chars, right)
```

**Update Methods**:
```python
def update_current_file(self, filename: str)
def update_line_col(self, line: int, col: int)  
def update_file_type(self, file_type: str)
```

**Real-time Updates**:
- Called every 0.1 seconds from EditorTabs
- Cursor position tracking
- File type detection from extensions

## 🔄 Data Flow

### File Opening Flow
```
1. User clicks file in FileTree
2. FileTree.on_tree_node_selected() triggered
3. Calls EditorTabs.open_file(path)
4. EditorTabs reads file content
5. Creates new tab with safe ID
6. Loads content into TextArea
7. Updates StatusBar with file info
8. Stores file data in open_files dict
```

### Tab Switching Flow
```
1. User clicks tab or uses keyboard
2. EditorTabs.switch_to_tab() called
3. Current content saved via save_current_tab_content()
4. Active tab styling updated
5. New tab content loaded into TextArea
6. StatusBar updated with new file info
7. current_tab variable updated
```

### Keyboard Shortcut Flow
```
1. User presses Control+N/W/S
2. TextEditor.on_key() receives event
3. Identifies shortcut and calls appropriate method
4. EditorTabs method executed
5. UI updated and user notified
6. Event marked as handled
```

## 🎨 Styling System

### CSS Organization
```python
CSS = """
/* Main Layout */
Screen { layout: vertical; }

/* Component Sections */
MenuBar { /* Purple theme */ }
FileTree { /* Cyan theme */ }  
EditorTabs { /* Green theme */ }
StatusBar { /* Orange theme */ }
"""
```

### Color Scheme
```python
COLORS = {
    "background": "#1a1a1a",
    "text": "#e0e0e0", 
    "menu": "#9d4edd",     # Purple
    "tree": "#00f5ff",     # Cyan
    "editor": "#39ff14",   # Green  
    "status": "#ff8c00"    # Orange
}
```

### Responsive Design
- Flexible layouts with `1fr` and percentage widths
- Min/max width constraints for tabs
- Horizontal scrolling for overflow
- Content alignment properties

## 🔧 Event System

### Event Types
1. **Click Events**: Tab switching, file opening, button clicks
2. **Key Events**: Global shortcuts, text input
3. **Tree Events**: Node expansion, selection
4. **Text Events**: Content changes, cursor movement
5. **Mount Events**: Component initialization

### Event Propagation
```python
# Event handling pattern
def on_event_type(self, event):
    try:
        # Handle event logic
        # Update UI state
        # Notify other components
        event.prevent_default()  # If needed
    except Exception as e:
        # Graceful error handling
        self.app.notify(f"Error: {e}", severity="error")
```

## 🗃️ State Management

### Application State
- **Root Path**: Working directory
- **Component References**: Query selectors for communication

### Component State
- **EditorTabs**: File data, current tab, counters
- **FileTree**: Tree structure, expanded nodes
- **StatusBar**: Display values, update timers

### State Synchronization
- Real-time updates via periodic callbacks
- Event-driven state changes
- Component communication through app queries

## 🚀 Performance Considerations

### Lazy Loading
- Directory contents loaded on demand
- Large files handled efficiently
- Memory usage optimized

### Update Frequency
- Status bar: 0.1 second intervals
- Content saving: On tab switch only
- UI updates: Event-driven

### Memory Management
- File content stored in memory for open tabs
- Closed tabs removed from memory
- Efficient string handling

## 🔒 Error Handling

### File System Errors
```python
try:
    content = file_path.read_text(encoding='utf-8')
except PermissionError:
    self.app.notify("Permission denied", severity="error")
except UnicodeDecodeError:
    self.app.notify("File encoding error", severity="error")
```

### UI Errors
- Graceful degradation for missing elements
- Try/except blocks around UI operations
- User-friendly error messages

### State Recovery
- Welcome tab as fallback
- Content persistence across errors
- Automatic cleanup of invalid states

## 🧪 Testing Strategy

### Manual Testing
```bash
# Development mode
textual run --dev editor.py

# Different directories
python editor.py /path/to/test

# Edge cases
python editor.py /root  # Permission issues
python editor.py /nonexistent  # Invalid path
```

### Test Cases
1. **File Operations**: Open, create, switch, close
2. **Keyboard Shortcuts**: All combinations
3. **Error Conditions**: Permissions, encoding, missing files
4. **UI Interactions**: Clicks, hovers, scrolling
5. **State Persistence**: Content saving, tab switching

## 📈 Scalability

### Adding Components
1. Create component class inheriting from Textual widget
2. Add to main layout in `compose()`
3. Define CSS styling in main CSS string
4. Implement event handlers
5. Add state management if needed

### Extending Functionality
- Plugin system architecture ready
- Event system supports new handlers
- CSS system supports new themes
- State management expandable

### Performance Scaling
- Lazy loading patterns established
- Memory management practices in place
- Efficient update mechanisms
- Modular architecture for optimization

---

This architecture supports the current feature set while providing a solid foundation for future enhancements.