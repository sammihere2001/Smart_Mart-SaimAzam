import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk
from utils.theme import Theme

class BaseView:
    def __init__(self, master, switch_callback):
        self.master = master
        self.switch_callback = switch_callback
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True)
        
        # Configure theme
        Theme.setup_styles()
        
        # Store loaded images as instance variables to prevent garbage collection
        self.images = {}
    
    def destroy(self):
        """Destroy the view frame"""
        self.frame.destroy()
    
    def show_error(self, message):
        """Show error messagebox
        
        Args:
            message (str): Error message to display
        """
        messagebox.showerror("Error", message)
    
    def show_info(self, message):
        """Show info messagebox
        
        Args:
            message (str): Info message to display
        """
        messagebox.showinfo("Information", message)
    
    def show_warning(self, message):
        """Show warning messagebox
        
        Args:
            message (str): Warning message to display
        """
        messagebox.showwarning("Warning", message)
    
    def confirm(self, message):
        """Show confirmation messagebox
        
        Args:
            message (str): Confirmation message to display
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        return messagebox.askyesno("Confirm", message)
    
    def load_and_resize_image(self, image_path, size):
        """Load and resize an image
        
        Args:
            image_path (str): Path to the image file
            size (tuple): Desired size (width, height)
            
        Returns:
            PhotoImage: Loaded and resized image or None if failed
        """
        try:
            # Get absolute path
            abs_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                image_path
            )
            
            if not os.path.exists(abs_path):
                return None
                
            # Open and resize image
            image = Image.open(abs_path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Store reference to prevent garbage collection
            self.images[image_path] = photo
            
            return photo
            
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    def create_styled_button(self, parent, text, command, width=None, bg=None, fg=None):
        """Create a styled button
        
        Args:
            parent (widget): Parent widget
            text (str): Button text
            command (function): Button command
            width (int, optional): Button width
            bg (str, optional): Button background color
            fg (str, optional): Button foreground color
            
        Returns:
            tk.Button: Styled button
        """
        style = "primary"
        if bg == Theme.SECONDARY:
            style = "secondary"
        elif bg == Theme.SUCCESS:
            style = "success"
        elif bg == Theme.DANGER:
            style = "danger"
            
        return Theme.create_button(parent, text, command, style=style, width=width)
    
    def create_styled_entry(self, parent, width=None, show=None):
        """Create a styled entry widget
        
        Args:
            parent: Parent widget
            width (int, optional): Entry width
            show (str, optional): Show character for password fields
            
        Returns:
            Entry: Styled entry widget
        """
        return Theme.create_entry(parent, width=width, show=show)
    
    def create_styled_label(self, parent, text, style="normal"):
        """Create a styled label
        
        Args:
            parent: Parent widget
            text (str): Label text
            style (str): Label style
            
        Returns:
            Label: Styled label
        """
        return Theme.create_label(parent, text, style=style)
    
    def create_section_frame(self, parent, title=None, padx=20, pady=20):
        """Create a styled section frame
        
        Args:
            parent: Parent widget
            title (str, optional): Section title
            padx (int): Horizontal padding
            pady (int): Vertical padding
            
        Returns:
            Frame: Styled frame
        """
        if title:
            frame = tk.LabelFrame(
                parent,
                text=title,
                font=Theme.FONT_MEDIUM_BOLD,
                bg=Theme.SURFACE,
                fg=Theme.TEXT,
                padx=padx,
                pady=pady
            )
        else:
            frame = tk.Frame(
                parent,
                bg=Theme.SURFACE,
                padx=padx,
                pady=pady
            )
            
        return frame
    
    def center_window(self, window, width, height):
        """Center a window on the screen
        
        Args:
            window (tk.Toplevel): Window to center
            width (int): Window width
            height (int): Window height
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_scrollable_frame(self, parent):
        """Create a scrollable frame
        
        Args:
            parent (widget): Parent widget
            
        Returns:
            tuple: (container_frame, scrollable_frame)
        """
        # Create a frame to hold the canvas and scrollbar
        container = tk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        # Configure scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        # Create window inside canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return container, scrollable_frame 