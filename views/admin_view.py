import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime, timedelta
from views.base_view import BaseView
from controllers.auth_controller import AuthController
from controllers.product_controller import ProductController
from controllers.sales_controller import SalesController

class AdminView(BaseView):
    def __init__(self, master, switch_callback, username):
        super().__init__(master, switch_callback)
        self.username = username
        self.auth_controller = AuthController()
        self.product_controller = ProductController()
        self.sales_controller = SalesController()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the admin UI"""
        # Configure the main frame
        self.frame.configure(bg="#f0f0f0")
        
        # Top panel with welcome message and logout button
        top_panel = tk.Frame(self.frame, bg="#4285f4", pady=10)
        top_panel.pack(fill=tk.X)
        
        welcome_label = tk.Label(
            top_panel, 
            text=f"Welcome, {self.username}!", 
            font=("Arial", 12, "bold"),
            bg="#4285f4",
            fg="white"
        )
        welcome_label.pack(side=tk.LEFT, padx=20)
        
        logout_button = self.create_styled_button(
            top_panel,
            text="Logout",
            command=self._logout,
            width=10,
            bg="#f44336",
            fg="white"
        )
        logout_button.pack(side=tk.RIGHT, padx=20)
        
        # Main content area with tabs
        tab_control = ttk.Notebook(self.frame)
        
        # Products tab
        products_tab = tk.Frame(tab_control, bg="white")
        tab_control.add(products_tab, text="Products")
        self._setup_products_tab(products_tab)
        
        # Cashiers tab
        cashiers_tab = tk.Frame(tab_control, bg="white")
        tab_control.add(cashiers_tab, text="Cashiers")
        self._setup_cashiers_tab(cashiers_tab)
        
        # Sales tab
        sales_tab = tk.Frame(tab_control, bg="white")
        tab_control.add(sales_tab, text="Sales Reports")
        self._setup_sales_tab(sales_tab)
        
        # Settings tab
        settings_tab = tk.Frame(tab_control, bg="white")
        tab_control.add(settings_tab, text="Settings")
        self._setup_settings_tab(settings_tab)
        
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
    def _setup_products_tab(self, parent):
        """Set up the products tab
        
        Args:
            parent (widget): Parent widget
        """
        # Create top toolbar with search and buttons
        toolbar = tk.Frame(parent, bg="white", pady=10)
        toolbar.pack(fill=tk.X)
        
        # Search frame
        search_frame = tk.Frame(toolbar, bg="white")
        search_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(search_frame, text="Search:", bg="white").pack(side=tk.LEFT)
        self.product_search = tk.Entry(search_frame, width=30)
        self.product_search.pack(side=tk.LEFT, padx=5)
        
        search_button = self.create_styled_button(
            search_frame,
            text="Search",
            command=self._search_products,
            width=8
        )
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Button frame
        button_frame = tk.Frame(toolbar, bg="white")
        button_frame.pack(side=tk.RIGHT, padx=10)
        
        add_button = self.create_styled_button(
            button_frame,
            text="Add Product",
            command=self._add_product,
            width=12
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        edit_button = self.create_styled_button(
            button_frame,
            text="Edit Product",
            command=self._edit_product,
            width=12,
            bg="#FF9800"
        )
        edit_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = self.create_styled_button(
            button_frame,
            text="Delete Product",
            command=self._delete_product,
            width=12,
            bg="#f44336"
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Create treeview for products
        columns = ("ID", "Category", "Name", "Price")
        self.product_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        # Configure columns
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Category", text="Category")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Price", text="Price")
        
        self.product_tree.column("ID", width=80)
        self.product_tree.column("Category", width=150)
        self.product_tree.column("Name", width=250)
        self.product_tree.column("Price", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.product_tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Load products
        self._load_products()
        
    def _load_products(self):
        """Load products into the treeview"""
        # Clear current items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        # Get products and add to treeview
        products = self.product_controller.get_all_products()
        for product in products:
            self.product_tree.insert("", "end", values=(
                product["id"], 
                product["category"], 
                product["name"], 
                f"${product['price']:.2f}"
            ))
    
    def _search_products(self):
        """Search for products"""
        search_term = self.product_search.get()
        
        # Clear current items
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
            
        # If search term is empty, load all products
        if not search_term:
            self._load_products()
            return
        
        # Search products
        products = self.product_controller.search_products(search_term)
        for product in products:
            self.product_tree.insert("", "end", values=(
                product["id"], 
                product["category"], 
                product["name"], 
                f"${product['price']:.2f}"
            ))
    
    def _add_product(self):
        """Add a new product"""
        # Open a new window to add product
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Product")
        add_window.geometry("400x300")
        add_window.resizable(False, False)
        self.center_window(add_window, 400, 300)
        
        # Form elements
        frame = tk.Frame(add_window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Product ID
        tk.Label(frame, text="Product ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        product_id = tk.Entry(frame, width=30)
        product_id.grid(row=0, column=1, pady=5)
        
        # Category
        tk.Label(frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category = tk.Entry(frame, width=30)
        category.grid(row=1, column=1, pady=5)
        
        # Name
        tk.Label(frame, text="Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        name = tk.Entry(frame, width=30)
        name.grid(row=2, column=1, pady=5)
        
        # Price
        tk.Label(frame, text="Price:").grid(row=3, column=0, sticky=tk.W, pady=5)
        price = tk.Entry(frame, width=30)
        price.grid(row=3, column=1, pady=5)
        
        # Add button
        add_button = self.create_styled_button(
            frame,
            text="Add Product",
            command=lambda: self._save_product(
                product_id.get(),
                category.get(),
                name.get(),
                price.get(),
                add_window
            ),
            width=15
        )
        add_button.grid(row=4, column=1, pady=20)
    
    def _save_product(self, product_id, category, name, price, window):
        """Save a new product
        
        Args:
            product_id (str): Product ID
            category (str): Product category
            name (str): Product name
            price (str): Product price
            window (Toplevel): The add product window
        """
        try:
            self.product_controller.add_product(product_id, category, name, price)
            self.show_info("Product added successfully")
            window.destroy()
            self._load_products()
        except ValueError as e:
            self.show_error(str(e))
    
    def _edit_product(self):
        """Edit selected product"""
        # Get selected item
        selected_item = self.product_tree.selection()
        if not selected_item:
            self.show_error("Please select a product to edit")
            return
        
        # Get product ID
        product_id = self.product_tree.item(selected_item[0], "values")[0]
        product = self.product_controller.get_product_by_id(product_id)
        
        # Open a new window to edit product
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Product")
        edit_window.geometry("400x300")
        edit_window.resizable(False, False)
        self.center_window(edit_window, 400, 300)
        
        # Form elements
        frame = tk.Frame(edit_window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Product ID (disabled)
        tk.Label(frame, text="Product ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        product_id_entry = tk.Entry(frame, width=30)
        product_id_entry.insert(0, product["id"])
        product_id_entry.config(state="disabled")
        product_id_entry.grid(row=0, column=1, pady=5)
        
        # Category
        tk.Label(frame, text="Category:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category = tk.Entry(frame, width=30)
        category.insert(0, product["category"])
        category.grid(row=1, column=1, pady=5)
        
        # Name
        tk.Label(frame, text="Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        name = tk.Entry(frame, width=30)
        name.insert(0, product["name"])
        name.grid(row=2, column=1, pady=5)
        
        # Price
        tk.Label(frame, text="Price:").grid(row=3, column=0, sticky=tk.W, pady=5)
        price = tk.Entry(frame, width=30)
        price.insert(0, product["price"])
        price.grid(row=3, column=1, pady=5)
        
        # Update button
        update_button = self.create_styled_button(
            frame,
            text="Update Product",
            command=lambda: self._update_product(
                product["id"],
                category.get(),
                name.get(),
                price.get(),
                edit_window
            ),
            width=15,
            bg="#FF9800"
        )
        update_button.grid(row=4, column=1, pady=20)
    
    def _update_product(self, product_id, category, name, price, window):
        """Update a product
        
        Args:
            product_id (str): Product ID
            category (str): Product category
            name (str): Product name
            price (str): Product price
            window (Toplevel): The edit product window
        """
        try:
            self.product_controller.update_product(product_id, category, name, price)
            self.show_info("Product updated successfully")
            window.destroy()
            self._load_products()
        except ValueError as e:
            self.show_error(str(e))
    
    def _delete_product(self):
        """Delete selected product"""
        # Get selected item
        selected_item = self.product_tree.selection()
        if not selected_item:
            self.show_error("Please select a product to delete")
            return
        
        # Get product ID
        product_id = self.product_tree.item(selected_item[0], "values")[0]
        
        # Confirm deletion
        if self.confirm(f"Are you sure you want to delete product {product_id}?"):
            try:
                self.product_controller.delete_product(product_id)
                self.show_info("Product deleted successfully")
                self._load_products()
            except ValueError as e:
                self.show_error(str(e))
    
    def _setup_cashiers_tab(self, parent):
        """Set up the cashiers tab
        
        Args:
            parent (widget): Parent widget
        """
        # Create top toolbar with buttons
        toolbar = tk.Frame(parent, bg="white", pady=10)
        toolbar.pack(fill=tk.X)
        
        # Button frame
        button_frame = tk.Frame(toolbar, bg="white")
        button_frame.pack(side=tk.RIGHT, padx=10)
        
        add_button = self.create_styled_button(
            button_frame,
            text="Add Cashier",
            command=self._add_cashier,
            width=12
        )
        add_button.pack(side=tk.LEFT, padx=5)
        
        update_button = self.create_styled_button(
            button_frame,
            text="Update Password",
            command=self._update_cashier_password,
            width=15,
            bg="#FF9800"
        )
        update_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = self.create_styled_button(
            button_frame,
            text="Delete Cashier",
            command=self._delete_cashier,
            width=12,
            bg="#f44336"
        )
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Create treeview for cashiers
        columns = ("Username",)
        self.cashier_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        # Configure columns
        self.cashier_tree.heading("Username", text="Username")
        self.cashier_tree.column("Username", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.cashier_tree.yview)
        self.cashier_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.cashier_tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Load cashiers
        self._load_cashiers()
    
    def _load_cashiers(self):
        """Load cashiers into the treeview"""
        # Clear current items
        for item in self.cashier_tree.get_children():
            self.cashier_tree.delete(item)
        
        # Get cashiers and add to treeview
        cashiers = self.auth_controller.get_all_cashiers()
        for cashier in cashiers:
            self.cashier_tree.insert("", "end", values=(cashier["username"],))
    
    def _add_cashier(self):
        """Add a new cashier"""
        # Open a new window to add cashier
        add_window = tk.Toplevel(self.master)
        add_window.title("Add Cashier")
        add_window.geometry("400x250")
        add_window.resizable(False, False)
        self.center_window(add_window, 400, 250)
        
        # Form elements
        frame = tk.Frame(add_window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Username
        tk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        username = tk.Entry(frame, width=30)
        username.grid(row=0, column=1, pady=5)
        
        # Password
        tk.Label(frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        password = tk.Entry(frame, width=30, show="*")
        password.grid(row=1, column=1, pady=5)
        
        # Confirm Password
        tk.Label(frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        confirm_password = tk.Entry(frame, width=30, show="*")
        confirm_password.grid(row=2, column=1, pady=5)
        
        # Add button
        add_button = self.create_styled_button(
            frame,
            text="Add Cashier",
            command=lambda: self._save_cashier(
                username.get(),
                password.get(),
                confirm_password.get(),
                add_window
            ),
            width=15
        )
        add_button.grid(row=3, column=1, pady=20)
    
    def _save_cashier(self, username, password, confirm_password, window):
        """Save a new cashier
        
        Args:
            username (str): Cashier username
            password (str): Cashier password
            confirm_password (str): Confirm password
            window (Toplevel): The add cashier window
        """
        try:
            self.auth_controller.add_cashier(username, password, confirm_password)
            self.show_info("Cashier added successfully")
            window.destroy()
            self._load_cashiers()
        except ValueError as e:
            self.show_error(str(e))
    
    def _update_cashier_password(self):
        """Update cashier password"""
        # Get selected item
        selected_item = self.cashier_tree.selection()
        if not selected_item:
            self.show_error("Please select a cashier")
            return
        
        # Get cashier username
        username = self.cashier_tree.item(selected_item[0], "values")[0]
        
        # Open a new window to update password
        update_window = tk.Toplevel(self.master)
        update_window.title("Update Cashier Password")
        update_window.geometry("400x200")
        update_window.resizable(False, False)
        self.center_window(update_window, 400, 200)
        
        # Form elements
        frame = tk.Frame(update_window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Username (disabled)
        tk.Label(frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        username_entry = tk.Entry(frame, width=30)
        username_entry.insert(0, username)
        username_entry.config(state="disabled")
        username_entry.grid(row=0, column=1, pady=5)
        
        # New Password
        tk.Label(frame, text="New Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        password = tk.Entry(frame, width=30, show="*")
        password.grid(row=1, column=1, pady=5)
        
        # Confirm Password
        tk.Label(frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        confirm_password = tk.Entry(frame, width=30, show="*")
        confirm_password.grid(row=2, column=1, pady=5)
        
        # Update button
        update_button = self.create_styled_button(
            frame,
            text="Update Password",
            command=lambda: self._save_cashier_password(
                username,
                password.get(),
                confirm_password.get(),
                update_window
            ),
            width=15,
            bg="#FF9800"
        )
        update_button.grid(row=3, column=1, pady=20)
    
    def _save_cashier_password(self, username, password, confirm_password, window):
        """Save cashier password
        
        Args:
            username (str): Cashier username
            password (str): Cashier password
            confirm_password (str): Confirm password
            window (Toplevel): The update password window
        """
        try:
            self.auth_controller.update_cashier_password(username, password, confirm_password)
            self.show_info("Password updated successfully")
            window.destroy()
        except ValueError as e:
            self.show_error(str(e))
    
    def _delete_cashier(self):
        """Delete selected cashier"""
        # Get selected item
        selected_item = self.cashier_tree.selection()
        if not selected_item:
            self.show_error("Please select a cashier")
            return
        
        # Get cashier username
        username = self.cashier_tree.item(selected_item[0], "values")[0]
        
        # Confirm deletion
        if self.confirm(f"Are you sure you want to delete cashier '{username}'?"):
            try:
                self.auth_controller.delete_cashier(username)
                self.show_info("Cashier deleted successfully")
                self._load_cashiers()
            except ValueError as e:
                self.show_error(str(e))
    
    def _setup_sales_tab(self, parent):
        """Set up the sales reports tab"""
        # Create main container
        main_frame = tk.Frame(parent, bg="white")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Date range selection
        date_frame = tk.Frame(main_frame, bg="white")
        date_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(date_frame, text="Date Range:", bg="white").pack(side="left", padx=5)
        
        # Create date range combobox
        self.date_range = ttk.Combobox(
            date_frame, 
            values=["Today", "Last 7 Days", "Last 30 Days", "This Month", "Last Month"],
            width=15,
            state="readonly"
        )
        self.date_range.set("Today")
        self.date_range.pack(side="left", padx=5)
        
        refresh_button = self.create_styled_button(
            date_frame,
            text="Refresh",
            command=self._refresh_sales_report,
            width=10
        )
        refresh_button.pack(side="left", padx=5)
        
        # Create notebook for different reports
        reports_notebook = ttk.Notebook(main_frame)
        reports_notebook.pack(fill="both", expand=True)
        
        # Summary tab
        summary_frame = tk.Frame(reports_notebook, bg="white")
        reports_notebook.add(summary_frame, text="Summary")
        
        # Summary cards
        summary_cards = tk.Frame(summary_frame, bg="white")
        summary_cards.pack(fill="x", pady=10)
        
        # Total Sales Card
        total_sales_card = tk.Frame(summary_cards, bg="#4285f4", padx=20, pady=10)
        total_sales_card.pack(side="left", padx=10, expand=True)
        tk.Label(
            total_sales_card,
            text="Total Sales",
            font=("Arial", 12, "bold"),
            bg="#4285f4",
            fg="white"
        ).pack()
        self.total_sales_label = tk.Label(
            total_sales_card,
            text="$0.00",
            font=("Arial", 16, "bold"),
            bg="#4285f4",
            fg="white"
        )
        self.total_sales_label.pack()
        
        # Total Transactions Card
        transactions_card = tk.Frame(summary_cards, bg="#0f9d58", padx=20, pady=10)
        transactions_card.pack(side="left", padx=10, expand=True)
        tk.Label(
            transactions_card,
            text="Transactions",
            font=("Arial", 12, "bold"),
            bg="#0f9d58",
            fg="white"
        ).pack()
        self.transactions_label = tk.Label(
            transactions_card,
            text="0",
            font=("Arial", 16, "bold"),
            bg="#0f9d58",
            fg="white"
        )
        self.transactions_label.pack()
        
        # Total Items Card
        items_card = tk.Frame(summary_cards, bg="#db4437", padx=20, pady=10)
        items_card.pack(side="left", padx=10, expand=True)
        tk.Label(
            items_card,
            text="Items Sold",
            font=("Arial", 12, "bold"),
            bg="#db4437",
            fg="white"
        ).pack()
        self.items_label = tk.Label(
            items_card,
            text="0",
            font=("Arial", 16, "bold"),
            bg="#db4437",
            fg="white"
        )
        self.items_label.pack()
        
        # Top Products tab
        products_frame = tk.Frame(reports_notebook, bg="white")
        reports_notebook.add(products_frame, text="Top Products")
        
        # Create treeview for top products
        columns = ("Rank", "Product", "Quantity", "Revenue")
        self.top_products_tree = ttk.Treeview(products_frame, columns=columns, show="headings")
        
        self.top_products_tree.heading("Rank", text="Rank")
        self.top_products_tree.heading("Product", text="Product")
        self.top_products_tree.heading("Quantity", text="Quantity")
        self.top_products_tree.heading("Revenue", text="Revenue")
        
        self.top_products_tree.column("Rank", width=50)
        self.top_products_tree.column("Product", width=200)
        self.top_products_tree.column("Quantity", width=100)
        self.top_products_tree.column("Revenue", width=100)
        
        self.top_products_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Category Analysis tab
        category_frame = tk.Frame(reports_notebook, bg="white")
        reports_notebook.add(category_frame, text="Category Analysis")
        
        # Create treeview for category analysis
        columns = ("Category", "Quantity", "Revenue", "Percentage")
        self.category_tree = ttk.Treeview(category_frame, columns=columns, show="headings")
        
        # Sales History tab
        history_frame = tk.Frame(reports_notebook, bg="white")
        reports_notebook.add(history_frame, text="Sales History")
        
        # Search and filter toolbar
        toolbar = tk.Frame(history_frame, bg="white", pady=10)
        toolbar.pack(fill=tk.X)
        
        # Search frame
        search_frame = tk.Frame(toolbar, bg="white")
        search_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(search_frame, text="Search:", bg="white").pack(side=tk.LEFT)
        self.history_search = tk.Entry(search_frame, width=30)
        self.history_search.pack(side=tk.LEFT, padx=5)
        
        search_button = self.create_styled_button(
            search_frame,
            text="Search",
            command=self._search_sales_history,
            width=8
        )
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Filter frame
        filter_frame = tk.Frame(toolbar, bg="white")
        filter_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(filter_frame, text="Filter by Cashier:", bg="white").pack(side=tk.LEFT)
        self.cashier_filter = ttk.Combobox(filter_frame, width=15, state="readonly")
        self.cashier_filter.pack(side=tk.LEFT, padx=5)
        
        # Create treeview for sales history
        columns = ("Date", "Bill ID", "Cashier", "Items", "Total")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("Bill ID", text="Bill ID")
        self.history_tree.heading("Cashier", text="Cashier")
        self.history_tree.heading("Items", text="Items")
        self.history_tree.heading("Total", text="Total")
        
        self.history_tree.column("Date", width=150)
        self.history_tree.column("Bill ID", width=100)
        self.history_tree.column("Cashier", width=100)
        self.history_tree.column("Items", width=200)
        self.history_tree.column("Total", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double click event for details
        self.history_tree.bind("<Double-1>", self._show_sale_details)
        
        self.category_tree.heading("Category", text="Category")
        self.category_tree.heading("Quantity", text="Quantity")
        self.category_tree.heading("Revenue", text="Revenue")
        self.category_tree.heading("Percentage", text="% of Total")
        
        self.category_tree.column("Category", width=150)
        self.category_tree.column("Quantity", width=100)
        self.category_tree.column("Revenue", width=100)
        self.category_tree.column("Percentage", width=100)
        
        self.category_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load initial data
        self._refresh_sales_report()
        
        # Bind date range change
        self.date_range.bind("<<ComboboxSelected>>", lambda e: self._refresh_sales_report())
        
        # Bind cashier filter change
        self.cashier_filter.bind("<<ComboboxSelected>>", lambda e: self._refresh_sales_history())
    
    def _get_date_range(self):
        """Get start and end dates based on selected range"""
        selection = self.date_range.get()
        end_date = datetime.now().date()
        
        if selection == "Today":
            start_date = end_date
        elif selection == "Last 7 Days":
            start_date = end_date - timedelta(days=6)
        elif selection == "Last 30 Days":
            start_date = end_date - timedelta(days=29)
        elif selection == "This Month":
            start_date = end_date.replace(day=1)
        else:  # Last Month
            if end_date.month == 1:
                start_date = end_date.replace(year=end_date.year-1, month=12, day=1)
                end_date = end_date.replace(year=end_date.year-1, month=12, day=31)
            else:
                start_date = end_date.replace(month=end_date.month-1, day=1)
                end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        return start_date, end_date
    
    def _refresh_sales_report(self):
        """Refresh all sales reports"""
        start_date, end_date = self._get_date_range()
        
        # Get sales data
        sales = self.sales_controller.get_sales_by_date_range(start_date, end_date)
        
        # Update summary
        total_sales = sum(sale["total"] for sale in sales)
        total_transactions = len(sales)
        total_items = sum(len(sale["items"]) for sale in sales)
        
        self.total_sales_label.config(text=f"${total_sales:.2f}")
        self.transactions_label.config(text=str(total_transactions))
        self.items_label.config(text=str(total_items))
        
        # Update top products
        top_products = self.sales_controller.get_top_selling_products(start_date, end_date)
        
        # Clear current items
        for item in self.top_products_tree.get_children():
            self.top_products_tree.delete(item)
            
        # Add new items
        for i, product in enumerate(top_products, 1):
            self.top_products_tree.insert("", "end", values=(
                i,
                product["product_name"],
                product["quantity"],
                f"${product['revenue']:.2f}"
            ))
        
        # Update category analysis
        category_sales = self.sales_controller.get_sales_by_category(start_date, end_date)
        
        # Clear current items
        for item in self.category_tree.get_children():
            self.category_tree.delete(item)
            
        # Add new items
        total_revenue = sum(cat["revenue"] for cat in category_sales.values())
        for category, data in category_sales.items():
            percentage = (data["revenue"] / total_revenue * 100) if total_revenue > 0 else 0
            self.category_tree.insert("", "end", values=(
                category,
                data["quantity"],
                f"${data['revenue']:.2f}",
                f"{percentage:.1f}%"
            ))
            
        # Update sales history
        self._refresh_sales_history()
    
    def _refresh_sales_history(self):
        """Refresh the sales history view"""
        start_date, end_date = self._get_date_range()
        sales = self.sales_controller.get_sales_by_date_range(start_date, end_date)
        
        # Update cashier filter
        cashiers = sorted(list(set(sale["cashier"] for sale in sales)))
        self.cashier_filter["values"] = ["All Cashiers"] + cashiers
        if not self.cashier_filter.get():
            self.cashier_filter.set("All Cashiers")
        
        # Apply filters
        selected_cashier = self.cashier_filter.get()
        search_term = self.history_search.get().lower()
        
        if selected_cashier != "All Cashiers":
            sales = [sale for sale in sales if sale["cashier"] == selected_cashier]
            
        if search_term:
            sales = [
                sale for sale in sales
                if search_term in sale["bill_id"].lower()
                or search_term in sale["cashier"].lower()
                or any(
                    search_term in item["name"].lower()
                    for item in sale["items"]
                )
            ]
        
        # Clear current items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Add filtered items
        for sale in reversed(sales):  # Show newest first
            date = datetime.fromisoformat(sale["date"]).strftime("%Y-%m-%d %H:%M:%S")
            items_text = ", ".join(f"{item['name']} (x{item['quantity']})" for item in sale["items"])
            if len(items_text) > 50:
                items_text = items_text[:47] + "..."
                
            self.history_tree.insert("", "end", values=(
                date,
                sale["bill_id"],
                sale["cashier"],
                items_text,
                f"${sale['total']:.2f}"
            ))
    
    def _search_sales_history(self):
        """Search sales history based on current filters"""
        self._refresh_sales_history()
    
    def _show_sale_details(self, event):
        """Show detailed information for a selected sale"""
        selected_item = self.history_tree.selection()
        if not selected_item:
            return
            
        # Get the bill ID from selected item
        bill_id = self.history_tree.item(selected_item[0], "values")[1]
        
        # Get all sales and find the matching one
        sales = self.sales_controller.get_all_sales()
        sale = next((s for s in sales if s["bill_id"] == bill_id), None)
        
        if not sale:
            return
            
        # Create details window
        details_window = tk.Toplevel(self.master)
        details_window.title(f"Sale Details - {bill_id}")
        details_window.geometry("500x400")
        details_window.resizable(False, False)
        self.center_window(details_window, 500, 400)
        
        # Sale information
        info_frame = tk.Frame(details_window, bg="white", padx=20, pady=10)
        info_frame.pack(fill="x")
        
        date = datetime.fromisoformat(sale["date"]).strftime("%Y-%m-%d %H:%M:%S")
        tk.Label(
            info_frame,
            text=f"Date: {date}",
            bg="white",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        tk.Label(
            info_frame,
            text=f"Bill ID: {sale['bill_id']}",
            bg="white",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        tk.Label(
            info_frame,
            text=f"Cashier: {sale['cashier']}",
            bg="white",
            font=("Arial", 10)
        ).pack(anchor="w")
        
        # Create treeview for items
        columns = ("Product", "Category", "Quantity", "Price", "Total")
        items_tree = ttk.Treeview(details_window, columns=columns, show="headings")
        
        items_tree.heading("Product", text="Product")
        items_tree.heading("Category", text="Category")
        items_tree.heading("Quantity", text="Quantity")
        items_tree.heading("Price", text="Price")
        items_tree.heading("Total", text="Total")
        
        items_tree.column("Product", width=150)
        items_tree.column("Category", width=100)
        items_tree.column("Quantity", width=70)
        items_tree.column("Price", width=80)
        items_tree.column("Total", width=80)
        
        # Add items
        for item in sale["items"]:
            items_tree.insert("", "end", values=(
                item["name"],
                item["category"],
                item["quantity"],
                f"${item['price']:.2f}",
                f"${item['total']:.2f}"
            ))
            
        items_tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Total
        total_frame = tk.Frame(details_window, bg="white", padx=20, pady=10)
        total_frame.pack(fill="x")
        
        tk.Label(
            total_frame,
            text=f"Total Amount: ${sale['total']:.2f}",
            bg="white",
            font=("Arial", 12, "bold")
        ).pack(side="right")
        
        # Close button
        close_button = self.create_styled_button(
            details_window,
            text="Close",
            command=details_window.destroy,
            width=10
        )
        close_button.pack(pady=10)
    
    def _setup_settings_tab(self, parent):
        """Set up the settings tab
        
        Args:
            parent (widget): Parent widget
        """
        # Change password frame
        frame = tk.LabelFrame(parent, text="Change Admin Password", padx=20, pady=20, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Current Password
        tk.Label(frame, text="Current Password:", bg="white").grid(row=0, column=0, sticky=tk.W, pady=5)
        current_password = tk.Entry(frame, width=30, show="*")
        current_password.grid(row=0, column=1, pady=5)
        
        # New Password
        tk.Label(frame, text="New Password:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
        new_password = tk.Entry(frame, width=30, show="*")
        new_password.grid(row=1, column=1, pady=5)
        
        # Confirm Password
        tk.Label(frame, text="Confirm Password:", bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
        confirm_password = tk.Entry(frame, width=30, show="*")
        confirm_password.grid(row=2, column=1, pady=5)
        
        # Change button
        change_button = self.create_styled_button(
            frame,
            text="Change Password",
            command=lambda: self._change_admin_password(
                current_password.get(),
                new_password.get(),
                confirm_password.get()
            ),
            width=15,
            bg="#673AB7"
        )
        change_button.grid(row=3, column=1, pady=20)
    
    def _change_admin_password(self, current_password, new_password, confirm_password):
        """Change admin password
        
        Args:
            current_password (str): Current password
            new_password (str): New password
            confirm_password (str): Confirm password
        """
        try:
            self.auth_controller.update_admin_password(
                self.username,
                current_password,
                new_password,
                confirm_password
            )
            self.show_info("Password changed successfully")
        except ValueError as e:
            self.show_error(str(e))
    
    def _logout(self):
        """Log out and return to login screen"""
        from views.login_view import LoginView
        self.switch_callback(LoginView) 