# Neon TUI Text Editor

A modern, VS Code-inspired TUI text editor built with Python and Textual, featuring a sleek neon-themed dark interface with rounded borders and real-time functionality.

![Neon Text Editor](screenshot.png)

## 🚀 Features

- **VS Code-like Interface**: Familiar layout with menu bar, file tree, tabbed editor, and status bar
- **Neon Dark Theme**: Beautiful dark theme with colored neon borders and rounded corners
- **File Management**: Browse and open files from directory tree with smart file type icons
- **Tabbed Editing**: Multiple file tabs with keyboard navigation and auto-scrolling
- **Line Numbers**: Built-in line numbers for code editing
- **Real-time Status**: Live cursor position and file type information
- **Text Editing**: Full text editing with undo/redo, cut/copy/paste, and select all
- **Keyboard Shortcuts**: Comprehensive keyboard shortcuts for productivity
- **Edit Menu**: Visual edit menu with all text editing options
- **Smart Icons**: File type-specific icons (Python 🐍, HTML 🌐, CSS 🎨, etc.)
- **Clean Interface**: Hidden scrollbars with functional navigation
- **Cross-platform**: Works on macOS, Linux, and Windows

## 📋 Requirements

- Python 3.9+
- Textual library
- pathlib (built-in)
- sys (built-in)
- os (built-in)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zeelsheladiya/neon-tui-text-editor.git
   cd text-editor
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install textual
   ```

## 🎮 Usage

### Basic Usage
```bash
# Run in current directory
python editor.py

# Run in specific directory
python editor.py /path/to/your/project

# Run in development mode (with debugging)
textual run --dev editor.py
```

### Keyboard Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Control+N` | New File | Create a new untitled file |
| `Control+W` | Close Tab | Close the currently active tab |
| `Control+S` | Save File | Save current file (placeholder) |
| `Control+J` | Previous Tab | Navigate to previous tab |
| `Control+L` | Next Tab | Navigate to next tab |
| `Control+Z` | Undo | Undo last action |
| `Control+U` | Redo | Redo last undone action |
| `Control+X` | Cut | Cut selected text to clipboard |
| `Control+C` | Copy | Copy selected text to clipboard |
| `Control+V` | Paste | Paste text from clipboard |
| `Control+A` | Select All | Select all text in editor |

### Interface Navigation

- **File Tree**: Click files to open them in tabs (smart icons show file types)
- **Tabs**: Click tabs to switch between files or use `Control+J/L` for keyboard navigation
- **New Tab**: Click the "+" button or use `Control+N`
- **Tab Navigation**: Use `Control+J` (previous) and `Control+L` (next) to navigate tabs
- **Auto-scrolling**: Tab bar automatically scrolls to show active tab
- **Text Editing**: Full clipboard integration with cut/copy/paste operations
- **Edit Menu**: Click "Edit" to see all available text editing options with shortcuts
- **Menu**: File and Edit menus (Edit menu fully functional)

## 🏗️ Project Structure

```
text-editor/
├── editor.py                 # Main application entry point
├── components/               # UI components
│   ├── header/
│   │   └── menubar.py       # Menu bar component (File, Edit)
│   ├── body/
│   │   ├── file_tree.py     # Directory tree component
│   │   └── editor_tabs.py   # Tabbed editor component
│   └── footer/
│       └── status_bar.py    # Status bar component
├── README.md                # This documentation
└── .venv/                   # Virtual environment (created after setup)
```

## 🧩 Architecture Overview

### Main Application (`editor.py`)
- **Entry Point**: Handles command-line arguments and app initialization
- **Layout Manager**: Defines the overall application layout
- **CSS Styling**: Contains all inline CSS for the neon theme
- **Keyboard Shortcuts**: Handles global keyboard shortcuts
- **Root Path Management**: Manages the working directory

### Component Architecture

#### 1. MenuBar (`components/header/menubar.py`)
- **Purpose**: Top navigation with File and Edit menus
- **Features**: Hover effects, expandable menu system
- **Future**: Ready for dropdown menus and additional options

#### 2. FileTree (`components/body/file_tree.py`)
- **Purpose**: Directory browser with expand/collapse functionality
- **Features**: 
  - Lazy loading of directories
  - File/folder icons (📁/📄)
  - Click-to-open functionality
  - Permission error handling
- **Data Structure**: Uses Textual Tree widget with custom data attributes

#### 3. EditorTabs (`components/body/editor_tabs.py`)
- **Purpose**: Multi-tab text editor with VS Code-like functionality
- **Features**:
  - Tab management with safe ID system
  - Content persistence between tab switches
  - Real-time status bar updates
  - File modification tracking
  - Horizontal scrolling for many tabs
- **Key Methods**:
  - `create_new_file()`: Creates untitled files
  - `open_file()`: Opens files from file tree
  - `switch_to_tab()`: Handles tab switching with content saving
  - `close_current_tab()`: Closes active tab via keyboard shortcut

#### 4. StatusBar (`components/footer/status_bar.py`)
- **Purpose**: Real-time information display
- **Information Shown**:
  - Current filename (orange highlight)
  - Cursor position (Ln X, Col Y)
  - File type/extension
- **Update Methods**: Real-time updates via periodic callbacks

## 🎨 Styling System

### Neon Theme Colors
- **Menu Bar**: Purple border (`#9d4edd`)
- **File Tree**: Cyan border (`#00f5ff`)
- **Editor Tabs**: Green border (`#39ff14`)
- **Status Bar**: Orange border (`#ff8c00`)
- **Background**: Dark (`#1a1a1a`)
- **Text**: Light gray (`#e0e0e0`)

### CSS Architecture
- **Inline CSS**: All styles defined in `editor.py` for easy maintenance
- **Component-specific**: Each component has dedicated CSS sections
- **Responsive**: Flexible layouts with proper width/height management
- **Rounded Borders**: `border: round` for modern appearance

## 🔧 Technical Implementation

### Safe ID System
Files with special characters (dots, spaces) are converted to safe HTML IDs:
```python
safe_id = filename.replace(".", "-").replace(" ", "-").replace("_", "-")
```
Example: `test.py` → `test-py`

### Content Persistence
Tab content is automatically saved when switching tabs:
```python
def save_current_tab_content(self):
    if self.current_tab and self.current_tab in self.open_files:
        editor = self.query_one("#editor-area")
        self.open_files[self.current_tab]["content"] = editor.text
```

### Real-time Updates
Status bar updates every 0.1 seconds with cursor position:
```python
self.set_interval(0.1, self.update_status_bar)
```

### File Management
Files are tracked in a dictionary structure:
```python
self.open_files[filename] = {
    "path": file_path,
    "content": content,
    "modified": False,
    "safe_id": safe_id
}
```

## 🚧 Development Guidelines

### Adding New Features

1. **New Components**: Create in appropriate `components/` subdirectory
2. **CSS Styling**: Add to the main CSS string in `editor.py`
3. **Event Handling**: Use Textual's event system (`on_click`, `on_key`, etc.)
4. **State Management**: Store state in component classes or main app

### Code Style
- **Type Hints**: Use for function parameters and returns
- **Docstrings**: Document all classes and methods
- **Error Handling**: Wrap risky operations in try/except blocks
- **Notifications**: Use `self.app.notify()` for user feedback

### Testing
```bash
# Development mode with live reload
textual run --dev editor.py

# Test with different directories
python editor.py /path/to/test/directory
```

## 🔮 Future Enhancements

### Planned Features
- [ ] **File Operations**: Save, Save As, Open File Dialog
- [ ] **Search & Replace**: Find/replace functionality
- [ ] **Syntax Highlighting**: Language-specific highlighting
- [ ] **Settings**: Customizable themes and preferences
- [ ] **Plugin System**: Extensible architecture
- [ ] **Git Integration**: Basic git status and operations
- [ ] **Multiple Panes**: Split editor views
- [ ] **Command Palette**: VS Code-style command interface

### Menu System Expansion
The current menu system is designed for easy expansion:
```python
# In menubar.py - ready for dropdown menus
def on_click(self, event):
    if event.widget.id == "file-menu":
        # Future: show file dropdown
    elif event.widget.id == "edit-menu":
        # Future: show edit dropdown
```

### Keyboard Shortcuts Expansion
Add new shortcuts in `editor.py`:
```python
def on_key(self, event):
    if event.key == "ctrl+o":
        # Open file dialog
    elif event.key == "ctrl+f":
        # Find/replace
```

## 🐛 Troubleshooting

### Common Issues

1. **CSS Errors**: Check for invalid Textual CSS properties
2. **File Permissions**: Ensure read access to target directories
3. **Tab Issues**: Verify safe ID generation for special filenames
4. **Layout Problems**: Check container hierarchy and CSS layout properties

### Debug Mode
Run with development mode for detailed error information:
```bash
textual run --dev editor.py
```

### Logging
Add debug notifications:
```python
self.app.notify(f"Debug: {variable_value}", severity="info")
```

## 📝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Follow** the existing code style
4. **Test** thoroughly with `textual run --dev`
5. **Document** new features
6. **Submit** a pull request

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- **Textual**: Amazing TUI framework by Textualize
- **VS Code**: Interface inspiration
- **Community**: For feedback and suggestions

---

*Built with ❤️ using Python and Textual*