import os
import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView
from views.admin_view import AdminView
from views.cashier_view import CashierView
from controllers.auth_controller import AuthController
from utils.theme import Theme

class LoginView(BaseView):
    def __init__(self, master, switch_callback):
        super().__init__(master, switch_callback)
        self.auth_controller = AuthController()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the login UI"""
        # Configure the main frame
        self.frame.configure(bg=Theme.BACKGROUND)
        
        # Create login container
        login_frame = tk.Frame(
            self.frame,
            bg=Theme.SURFACE,
            padx=40,
            pady=30,
            relief=tk.RAISED,
            borderwidth=1
        )
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo and title
        title_frame = tk.Frame(login_frame, bg=Theme.SURFACE)
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Load and display logo
        logo = self.load_and_resize_image("assets/logo.png", (80, 80))
        if logo:
            logo_label = tk.Label(title_frame, image=logo, bg=Theme.SURFACE)
            logo_label.image = logo
            logo_label.pack()
        
        # Title
        Theme.create_label(
            title_frame,
            text="Smart Mart",
            style="large_bold"
        ).pack(pady=(10, 0))
        
        Theme.create_label(
            title_frame,
            text="Management System",
            style="secondary"
        ).pack()
        
        # Username
        Theme.create_label(
            login_frame,
            text="Username",
            style="bold"
        ).pack(anchor=tk.W)
        
        self.username = Theme.create_entry(login_frame, width=30)
        self.username.pack(fill=tk.X, pady=(5, 15))
        
        # Password
        Theme.create_label(
            login_frame,
            text="Password",
            style="bold"
        ).pack(anchor=tk.W)
        
        self.password = Theme.create_entry(login_frame, width=30, show="*")
        self.password.pack(fill=tk.X, pady=(5, 25))
        
        # Login button
        login_button = Theme.create_button(
            login_frame,
            text="Login",
            command=self._login,
            style="primary",
            width=20
        )
        login_button.pack(pady=(0, 15))
        
        # Error message label
        self.error_label = Theme.create_label(
            login_frame,
            text="",
            style="secondary"
        )
        self.error_label.pack()
        
        # Bind enter key to login
        self.username.bind("<Return>", lambda e: self._login())
        self.password.bind("<Return>", lambda e: self._login())
        
        # Focus username entry
        self.username.focus()
    
    def _login(self):
        """Handle login attempt"""
        username = self.username.get()
        password = self.password.get()
        
        try:
            user_type = self.auth_controller.login(username, password)
            
            if user_type == "admin":
                self.switch_callback(AdminView, username)
            else:
                self.switch_callback(CashierView, username)
                
        except ValueError as e:
            self.error_label.config(
                text=str(e),
                fg=Theme.DANGER
            )
            self.password.delete(0, tk.END)
            self.password.focus() 