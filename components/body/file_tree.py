from pathlib import Path
from textual.widgets import Tree
from textual.reactive import reactive


class FileTree(Tree):
    """File directory tree component"""
    
    def __init__(self, root_path: Path, **kwargs):
        super().__init__("Files", **kwargs)
        self.root_path = root_path
        self.show_root = False
        
    def on_mount(self):
        """Initialize the file tree when mounted"""
        self.load_directory(self.root_path, self.root)
        
    def load_directory(self, path: Path, node):
        """Load directory contents into tree node"""
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in items:
                if item.name.startswith('.'):
                    continue
                    
                if item.is_dir():
                    # Use better folder icon
                    dir_node = node.add(f"🗂️  {item.name}", data={"path": item, "type": "directory"})
                    # Add a placeholder for lazy loading
                    dir_node.add("Loading...", data={"type": "placeholder"})
                else:
                    # Use better file icons based on extension
                    icon = self.get_file_icon(item)
                    file_node = node.add(f"{icon}  {item.name}", data={"path": item, "type": "file"})
                    # Disable expand/collapse for files
                    file_node.allow_expand = False
                    
        except PermissionError:
            node.add("Permission Denied", data={"type": "error"})
    
    def on_tree_node_expanded(self, event):
        """Handle directory expansion"""
        node = event.node
        if node.data and node.data.get("type") == "directory":
            # Clear placeholder and load actual contents
            node.remove_children()
            self.load_directory(node.data["path"], node)
    
    def get_file_icon(self, file_path: Path) -> str:
        """Get appropriate icon for file based on extension"""
        extension = file_path.suffix.lower()
        
        # Programming files
        if extension in ['.py']:
            return '🐍'  # Python
        elif extension in ['.js', '.jsx']:
            return '📜'  # JavaScript
        elif extension in ['.ts', '.tsx']:
            return '📘'  # TypeScript
        elif extension in ['.html', '.htm']:
            return '🌐'  # HTML
        elif extension in ['.css', '.scss', '.sass']:
            return '🎨'  # CSS
        elif extension in ['.json']:
            return '📋'  # JSON
        elif extension in ['.xml']:
            return '📄'  # XML
        elif extension in ['.md', '.markdown']:
            return '📝'  # Markdown
        elif extension in ['.txt']:
            return '📃'  # Text
        elif extension in ['.yml', '.yaml']:
            return '⚙️'   # YAML
        elif extension in ['.toml']:
            return '🔧'  # TOML
        elif extension in ['.ini', '.cfg', '.conf']:
            return '⚙️'   # Config
        # Image files
        elif extension in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico']:
            return '🖼️'   # Images
        # Archive files
        elif extension in ['.zip', '.tar', '.gz', '.rar', '.7z']:
            return '📦'  # Archives
        # Executable files
        elif extension in ['.exe', '.app', '.deb', '.rpm']:
            return '⚡'  # Executables
        # Default file icon
        else:
            return '📄'  # Generic file
    
    def on_tree_node_selected(self, event):
        """Handle file/directory selection"""
        node = event.node
        if node.data and node.data.get("type") == "file":
            # Open file in editor
            file_path = node.data["path"]
            try:
                editor_tabs = self.app.query_one("#editor-tabs")
                editor_tabs.open_file(file_path)
                self.app.notify(f"Opening file: {file_path.name}")
            except Exception as e:
                self.app.notify(f"Error opening file: {e}", severity="error")