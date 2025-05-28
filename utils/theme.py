from tkinter import ttk
import tkinter as tk

class Theme:
    # Color Scheme
    PRIMARY = "#1976D2"  # Blue
    PRIMARY_LIGHT = "#2196F3"
    PRIMARY_DARK = "#0D47A1"
    
    SECONDARY = "#FF9800"  # Orange
    SECONDARY_LIGHT = "#FFB74D"
    SECONDARY_DARK = "#F57C00"
    
    SUCCESS = "#4CAF50"  # Green
    SUCCESS_LIGHT = "#81C784"
    SUCCESS_DARK = "#388E3C"
    
    DANGER = "#F44336"  # Red
    DANGER_LIGHT = "#E57373"
    DANGER_DARK = "#D32F2F"
    
    WARNING = "#FFC107"  # Amber
    INFO = "#2196F3"     # Light Blue
    
    BACKGROUND = "#F5F5F5"  # Light Grey
    SURFACE = "#FFFFFF"     # White
    TEXT = "#212121"        # Dark Grey
    TEXT_SECONDARY = "#757575"  # Medium Grey
    BORDER = "#E0E0E0"      # Light Grey
    
    # Font Configurations
    FONT_FAMILY = "Segoe UI"
    FONT_LARGE = (FONT_FAMILY, 14)
    FONT_MEDIUM = (FONT_FAMILY, 12)
    FONT_SMALL = (FONT_FAMILY, 10)
    FONT_LARGE_BOLD = (FONT_FAMILY, 14, "bold")
    FONT_MEDIUM_BOLD = (FONT_FAMILY, 12, "bold")
    FONT_SMALL_BOLD = (FONT_FAMILY, 10, "bold")
    
    # Widget Styles
    BUTTON_STYLE = {
        "font": FONT_MEDIUM,
        "borderwidth": 0,
        "relief": tk.FLAT,
        "cursor": "hand2",
        "padx": 15,
        "pady": 8
    }
    
    ENTRY_STYLE = {
        "font": FONT_MEDIUM,
        "relief": tk.SOLID,
        "borderwidth": 1
    }
    
    LABEL_STYLE = {
        "font": FONT_MEDIUM,
        "background": SURFACE
    }
    
    @classmethod
    def setup_styles(cls):
        """Configure ttk styles for the application"""
        style = ttk.Style()
        
        # Treeview
        style.configure(
            "Treeview",
            background=cls.SURFACE,
            fieldbackground=cls.SURFACE,
            foreground=cls.TEXT,
            font=cls.FONT_MEDIUM,
            rowheight=30
        )
        
        style.configure(
            "Treeview.Heading",
            background=cls.PRIMARY_LIGHT,
            foreground="white",
            font=cls.FONT_MEDIUM_BOLD,
            relief="flat"
        )
        
        style.map(
            "Treeview",
            background=[("selected", cls.PRIMARY)],
            foreground=[("selected", "white")]
        )
        
        # Notebook (Tabs)
        style.configure(
            "TNotebook",
            background=cls.BACKGROUND,
            borderwidth=0
        )
        
        style.configure(
            "TNotebook.Tab",
            background=cls.BACKGROUND,
            foreground=cls.TEXT,
            padding=[10, 5],
            font=cls.FONT_MEDIUM
        )
        
        style.map(
            "TNotebook.Tab",
            background=[("selected", cls.PRIMARY)],
            foreground=[("selected", "white"), ("!selected", cls.TEXT)]
        )
        
        # Combobox
        style.configure(
            "TCombobox",
            background=cls.SURFACE,
            fieldbackground=cls.SURFACE,
            selectbackground=cls.PRIMARY,
            selectforeground="white",
            padding=5
        )
        
        # Scrollbar
        style.configure(
            "TScrollbar",
            background=cls.SURFACE,
            troughcolor=cls.BACKGROUND,
            width=12,
            arrowsize=13
        )
    
    @classmethod
    def create_button(cls, parent, text, command, style="primary", width=None):
        """Create a styled button
        
        Args:
            parent: Parent widget
            text (str): Button text
            command: Button command
            style (str): Button style (primary, secondary, success, danger)
            width (int, optional): Button width
            
        Returns:
            tk.Button: Styled button
        """
        styles = {
            "primary": (cls.PRIMARY, cls.PRIMARY_DARK, "white"),
            "secondary": (cls.SECONDARY, cls.SECONDARY_DARK, "white"),
            "success": (cls.SUCCESS, cls.SUCCESS_DARK, "white"),
            "danger": (cls.DANGER, cls.DANGER_DARK, "white")
        }
        
        bg, active_bg, fg = styles.get(style, styles["primary"])
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            width=width,
            **cls.BUTTON_STYLE
        )
        
        return button
    
    @classmethod
    def create_entry(cls, parent, width=None, show=None):
        """Create a styled entry widget"""
        entry = tk.Entry(
            parent,
            bg=cls.SURFACE,
            fg=cls.TEXT,
            insertbackground=cls.TEXT,
            width=width,
            show=show,
            **cls.ENTRY_STYLE
        )
        
        return entry
    
    @classmethod
    def create_label(cls, parent, text, style="normal"):
        """Create a styled label"""
        styles = {
            "normal": {"font": cls.FONT_MEDIUM, "fg": cls.TEXT},
            "bold": {"font": cls.FONT_MEDIUM_BOLD, "fg": cls.TEXT},
            "large": {"font": cls.FONT_LARGE, "fg": cls.TEXT},
            "large_bold": {"font": cls.FONT_LARGE_BOLD, "fg": cls.TEXT},
            "secondary": {"font": cls.FONT_MEDIUM, "fg": cls.TEXT_SECONDARY}
        }
        
        style_config = styles.get(style, styles["normal"])
        label_config = {**cls.LABEL_STYLE, **style_config}
        
        label = tk.Label(
            parent,
            text=text,
            **label_config
        )
        
        return label 