import os
import sys
import tkinter as tk
from views.login_view import LoginView
from utils.theme import Theme

class SmartMartApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Mart Management System")
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
        
        # Set window icon
        icon_path = os.path.join("assets", "icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # Configure theme
        self.root.configure(bg=Theme.BACKGROUND)
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1024) // 2
        y = (screen_height - 768) // 2
        self.root.geometry(f"1024x768+{x}+{y}")
        
        # Initialize the login view
        self.current_view = LoginView(self.root, self.switch_view)
        
    def switch_view(self, view_class, *args, **kwargs):
        """Switch between different views in the application"""
        # Destroy current view
        if hasattr(self, 'current_view') and self.current_view is not None:
            self.current_view.destroy()
            
        # Create new view
        self.current_view = view_class(self.root, self.switch_view, *args, **kwargs)
        
    def run(self):
        """Run the application main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    # Add path to project root for imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Create and run the application
    app = SmartMartApp()
    app.run() 