# Development Guide

## 🛠️ Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- Terminal/Command Line access

### Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd text-editor

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install textual

# Verify installation
python editor.py --help
```

### Development Mode
```bash
# Run with live reload and debugging
textual run --dev editor.py

# Run with specific directory
textual run --dev editor.py /path/to/test/directory
```

## 🏗️ Adding New Features

### 1. Creating New Components

#### Step 1: Create Component File
```python
# components/new_feature/my_component.py
from textual.widgets import Static
from textual.containers import Vertical

class MyComponent(Static):
    """Description of what this component does"""
    
    def compose(self):
        with Vertical():
            yield Static("My Component Content")
    
    def on_mount(self):
        """Initialize component when mounted"""
        pass
    
    def on_click(self, event):
        """Handle click events"""
        pass
```

#### Step 2: Add to Main Layout
```python
# In editor.py compose() method
def compose(self):
    # ... existing components
    yield MyComponent(id="my-component")
```

#### Step 3: Add CSS Styling
```python
# In editor.py CSS string
CSS = """
/* Existing styles... */

/* My Component */
MyComponent {
    background: #1a1a1a;
    color: #e0e0e0;
    border: round #ff6b6b;  /* Choose your neon color */
    margin: 1;
}

#my-component {
    height: auto;
    width: 100%;
}
"""
```

### 2. Adding Keyboard Shortcuts

```python
# In editor.py on_key() method
def on_key(self, event):
    # Existing shortcuts...
    elif event.key == "ctrl+your_key":
        # Your functionality here
        component = self.query_one("#your-component")
        component.your_method()
        event.prevent_default()
```

#### Current Shortcuts:
- `Control+N`: New file
- `Control+W`: Close tab
- `Control+S`: Save file
- `Control+J`: Previous tab
- `Control+L`: Next tab
- `Control+Z`: Undo
- `Control+U`: Redo
- `Control+X`: Cut
- `Control+C`: Copy
- `Control+V`: Paste
- `Control+A`: Select all

### 3. Adding Menu Items

```python
# In components/header/menubar.py
def compose(self):
    with Horizontal():
        yield Static("File", classes="menu-item", id="file-menu")
        yield Static("Edit", classes="menu-item", id="edit-menu")
        yield Static("View", classes="menu-item", id="view-menu")  # New menu
        yield Static("Text Editor", classes="title")

def on_click(self, event):
    # Existing handlers...
    elif event.widget.id == "view-menu":
        self.app.notify("View menu clicked")
        # Future: implement dropdown
```

## 🎨 Styling Guidelines

### Color Scheme
Use the established neon color palette:
```python
NEON_COLORS = {
    "purple": "#9d4edd",   # Menu bar
    "cyan": "#00f5ff",     # File tree  
    "green": "#39ff14",    # Editor tabs
    "orange": "#ff8c00",   # Status bar
    "red": "#ff073a",      # Close buttons/errors
    "pink": "#ff6b6b",     # Available for new features
    "yellow": "#ffff00",   # Available for new features
    "blue": "#00bfff"      # Available for new features
}
```

### CSS Best Practices
```css
/* Component styling template */
ComponentName {
    background: #1a1a1a;           /* Dark background */
    color: #e0e0e0;                /* Light text */
    border: round #your_color;      /* Rounded neon border */
    margin: 1;                     /* Standard margin */
    padding: 1;                    /* Standard padding */
}

/* Interactive elements */
.interactive-element:hover {
    background: #your_color 20%;   /* Subtle hover effect */
    color: #ffffff;                /* Bright text on hover */
}

/* Active states */
.active {
    background: #your_color 30%;   /* More prominent active state */
    text-style: bold;              /* Bold text for active items */
}
```

### Layout Patterns
```css
/* Horizontal layouts */
.horizontal-container {
    layout: horizontal;
    height: 3;                     /* Standard height for bars */
}

/* Vertical layouts */
.vertical-container {
    layout: vertical;
    height: 1fr;                   /* Fill available space */
}

/* Flexible widths */
.flexible-width {
    width: 1fr;                    /* Take remaining space */
}

/* Fixed widths */
.fixed-width {
    width: 20;                     /* Fixed character width */
    min-width: 15;                 /* Minimum width */
    max-width: 30;                 /* Maximum width */
}
```

## 🔧 Component Communication

### Parent-Child Communication
```python
# Parent accessing child
child_component = self.query_one("#child-id")
child_component.update_data(new_data)

# Child accessing parent
parent_app = self.app
parent_app.notify("Message from child")
```

### Cross-Component Communication
```python
# Via main app
def communicate_between_components(self):
    source = self.query_one("#source-component")
    target = self.query_one("#target-component")
    
    data = source.get_data()
    target.update_with_data(data)
```

### Event Broadcasting
```python
# Custom events
from textual.message import Message

class CustomEvent(Message):
    def __init__(self, data):
        super().__init__()
        self.data = data

# Send event
self.post_message(CustomEvent("some data"))

# Handle event
def on_custom_event(self, event: CustomEvent):
    # Handle the event
    pass
```

## 🧪 Testing Your Changes

### Manual Testing Checklist
- [ ] Component renders correctly
- [ ] Styling matches neon theme
- [ ] Keyboard shortcuts work (Control+N/W/S/J/L/Z/U/X/C/V/A)
- [ ] Tab navigation and auto-scrolling works
- [ ] Text editing operations (cut/copy/paste/undo/redo/select all)
- [ ] Edit menu displays and functions correctly
- [ ] Clipboard integration works with other applications
- [ ] File icons display correctly for different file types
- [ ] Files don't show expand/collapse arrows
- [ ] Folders show expand/collapse arrows
- [ ] No console errors
- [ ] Responsive layout
- [ ] Error handling works
- [ ] Performance is acceptable

### Testing Commands
```bash
# Basic functionality
python editor.py

# Test with different directories
python editor.py /
python editor.py ~/Documents
python editor.py /nonexistent  # Should handle gracefully

# Development mode with debugging
textual run --dev editor.py

# Test keyboard shortcuts
# Control+N, Control+W, Control+S

# Test file operations
# Click files in tree, switch tabs, create new files
```

### Debug Techniques
```python
# Add debug notifications
self.app.notify(f"Debug: {variable_value}", severity="info")

# Console logging (visible in dev mode)
print(f"Debug: {variable_value}")

# Textual console (dev mode)
# Press Ctrl+\ to open Textual console
```

## 📝 Code Style Guidelines

### Python Style
```python
# Type hints
def my_function(param: str, optional: int = 0) -> bool:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
        optional: Description with default value
        
    Returns:
        Description of return value
    """
    return True

# Class structure
class MyComponent(Static):
    """Component description."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_state = {}
    
    def compose(self):
        """Define component layout."""
        # Layout code here
    
    def on_mount(self):
        """Initialize when mounted."""
        # Initialization code
    
    # Event handlers
    def on_click(self, event):
        """Handle click events."""
        # Event handling code
```

### Error Handling
```python
# Standard error handling pattern
def risky_operation(self):
    try:
        # Risky code here
        result = potentially_failing_operation()
        return result
    except SpecificException as e:
        self.app.notify(f"Specific error: {e}", severity="error")
        return default_value
    except Exception as e:
        self.app.notify(f"Unexpected error: {e}", severity="error")
        return default_value
```

### State Management
```python
# Component state pattern
class MyComponent(Static):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize state
        self.data = {}
        self.current_item = None
        self.is_active = False
    
    def update_state(self, new_data):
        """Update component state and refresh UI."""
        self.data.update(new_data)
        self.refresh_display()
    
    def refresh_display(self):
        """Update UI based on current state."""
        # Update UI elements
        pass
```

## 🚀 Performance Guidelines

### Efficient Updates
```python
# Good: Batch updates
def update_multiple_items(self, items):
    for item in items:
        self.process_item(item)
    self.refresh()  # Single refresh at end

# Avoid: Multiple individual updates
def update_multiple_items_bad(self, items):
    for item in items:
        self.process_item(item)
        self.refresh()  # Refresh for each item
```

### Memory Management
```python
# Clean up resources
def cleanup(self):
    # Clear large data structures
    self.large_data.clear()
    
    # Remove event handlers if needed
    # Cancel timers
    if hasattr(self, 'timer'):
        self.timer.cancel()
```

### Lazy Loading
```python
# Load data only when needed
def load_data_on_demand(self):
    if not hasattr(self, '_cached_data'):
        self._cached_data = expensive_operation()
    return self._cached_data
```

## 🐛 Debugging Common Issues

### CSS Not Applied
1. Check CSS syntax (no invalid properties)
2. Verify component IDs and classes
3. Check CSS selector specificity
4. Use dev mode to inspect styles

### Component Not Rendering
1. Check `compose()` method returns widgets
2. Verify component is yielded in parent
3. Check for exceptions in `on_mount()`
4. Ensure proper inheritance

### Events Not Working
1. Verify event handler method names
2. Check `event.prevent_default()` usage
3. Ensure component can receive focus
4. Check event propagation

### Layout Issues
1. Check container types (Vertical/Horizontal)
2. Verify width/height properties
3. Check for conflicting CSS rules
4. Test with different content sizes

## 🎨 File Icon System

The file tree uses smart icons based on file extensions:

```python
# File type icons
ICONS = {
    '.py': '🐍',      # Python
    '.js': '📜',      # JavaScript  
    '.ts': '📘',      # TypeScript
    '.html': '🌐',    # HTML
    '.css': '🎨',     # CSS
    '.json': '📋',    # JSON
    '.md': '📝',      # Markdown
    '.txt': '📃',     # Text
    '.yml': '⚙️',     # YAML
    '.png': '🖼️',     # Images
    '.zip': '📦',     # Archives
    '.exe': '⚡',     # Executables
    # ... more types
}
```

### Adding New File Types
To add support for new file extensions:

1. **Update `get_file_icon()` method** in `components/body/file_tree.py`
2. **Add new extension** to appropriate category
3. **Choose appropriate emoji** that represents the file type
4. **Test with actual files** of that type

## 📚 Useful Resources

### Textual Documentation
- [Official Textual Docs](https://textual.textualize.io/)
- [Widget Reference](https://textual.textualize.io/widget_gallery/)
- [CSS Reference](https://textual.textualize.io/styles/)
- [Event System](https://textual.textualize.io/events/)

### Development Tools
```bash
# Textual development console
textual console

# Live CSS editing
textual run --dev --css-hot-reload editor.py

# Widget inspector
# Press Ctrl+\ in dev mode
```

### Example Implementations
Look at existing components for patterns:
- `EditorTabs`: Complex state management
- `FileTree`: Tree widget usage
- `StatusBar`: Real-time updates
- `MenuBar`: Simple click handling

## 🤝 Contributing Workflow

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/my-feature`
3. **Develop** following these guidelines
4. **Test** thoroughly
5. **Document** changes
6. **Commit** with clear messages
7. **Push** and create pull request

### Commit Message Format
```
type(scope): brief description

Longer description if needed

- List of changes
- Another change
```

Example:
```
feat(editor): add syntax highlighting support

Implement basic syntax highlighting for Python files
using Pygments library integration.

- Add syntax highlighter component
- Integrate with editor tabs
- Add language detection
- Update styling for highlighted code
```

---

Happy coding! 🚀