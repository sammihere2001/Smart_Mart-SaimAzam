import tkinter as tk
from tkinter import ttk
import json
from views.base_view import BaseView
from controllers.product_controller import ProductController
from controllers.billing_controller import BillingController

class CashierView(BaseView):
    def __init__(self, master, switch_callback, username):
        super().__init__(master, switch_callback)
        self.username = username
        self.product_controller = ProductController()
        self.billing_controller = BillingController()
        self.cart_items = []  # List to store items in cart
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the cashier UI"""
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
        
        # Billing tab
        billing_tab = tk.Frame(tab_control, bg="white")
        tab_control.add(billing_tab, text="Billing")
        self._setup_billing_tab(billing_tab)
        
        # Sales History tab
        history_tab = tk.Frame(tab_control, bg="white")
        tab_control.add(history_tab, text="Sales History")
        self._setup_history_tab(history_tab)
        
        tab_control.pack(expand=1, fill="both", padx=10, pady=10)
    
    def _setup_billing_tab(self, parent):
        """Set up the billing tab
        
        Args:
            parent (widget): Parent widget
        """
        # Create left panel for products
        left_panel = tk.Frame(parent, bg="white")
        left_panel.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Create right panel for cart
        right_panel = tk.Frame(parent, bg="white")
        right_panel.pack(side=tk.RIGHT, fill="both", expand=True)
        
        # Products section
        products_frame = tk.LabelFrame(left_panel, text="Products", padx=10, pady=10, bg="white")
        products_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Search frame
        search_frame = tk.Frame(products_frame, bg="white")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
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
        
        # Create treeview for products
        columns = ("ID", "Category", "Name", "Price")
        self.product_tree = ttk.Treeview(products_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Category", text="Category")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Price", text="Price")
        
        self.product_tree.column("ID", width=60)
        self.product_tree.column("Category", width=100)
        self.product_tree.column("Name", width=150)
        self.product_tree.column("Price", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(products_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.product_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Add to cart button
        add_to_cart_frame = tk.Frame(left_panel, bg="white", pady=10)
        add_to_cart_frame.pack(fill=tk.X)
        
        tk.Label(add_to_cart_frame, text="Quantity:", bg="white").pack(side=tk.LEFT, padx=(10, 5))
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = tk.Entry(add_to_cart_frame, textvariable=self.quantity_var, width=5)
        quantity_entry.pack(side=tk.LEFT, padx=5)
        
        add_to_cart_button = self.create_styled_button(
            add_to_cart_frame,
            text="Add to Cart",
            command=self._add_to_cart,
            width=15
        )
        add_to_cart_button.pack(side=tk.RIGHT, padx=10)
        
        # Load products
        self._load_products()
        
        # Cart section
        cart_frame = tk.LabelFrame(right_panel, text="Shopping Cart", padx=10, pady=10, bg="white")
        cart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for cart
        columns = ("ID", "Name", "Price", "Quantity", "Total")
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.cart_tree.heading("ID", text="ID")
        self.cart_tree.heading("Name", text="Name")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Quantity", text="Qty")
        self.cart_tree.heading("Total", text="Total")
        
        self.cart_tree.column("ID", width=60)
        self.cart_tree.column("Name", width=150)
        self.cart_tree.column("Price", width=80)
        self.cart_tree.column("Quantity", width=50)
        self.cart_tree.column("Total", width=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=self.cart_tree.yview)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.cart_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Cart buttons
        cart_buttons_frame = tk.Frame(right_panel, bg="white", pady=10)
        cart_buttons_frame.pack(fill=tk.X)
        
        remove_button = self.create_styled_button(
            cart_buttons_frame,
            text="Remove Item",
            command=self._remove_from_cart,
            width=12,
            bg="#f44336"
        )
        remove_button.pack(side=tk.LEFT, padx=10)
        
        clear_button = self.create_styled_button(
            cart_buttons_frame,
            text="Clear Cart",
            command=self._clear_cart,
            width=12,
            bg="#FF9800"
        )
        clear_button.pack(side=tk.LEFT, padx=10)
        
        # Total and checkout
        total_frame = tk.Frame(right_panel, bg="white", pady=10)
        total_frame.pack(fill=tk.X)
        
        tk.Label(
            total_frame,
            text="Total: ",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT, padx=10)
        
        self.total_var = tk.StringVar(value="$0.00")
        tk.Label(
            total_frame,
            textvariable=self.total_var,
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(side=tk.LEFT)
        
        checkout_button = self.create_styled_button(
            total_frame,
            text="Checkout",
            command=self._checkout,
            width=15,
            bg="#4CAF50"
        )
        checkout_button.pack(side=tk.RIGHT, padx=10)
    
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
    
    def _add_to_cart(self):
        """Add selected product to cart"""
        # Get selected product
        selected_item = self.product_tree.selection()
        if not selected_item:
            self.show_error("Please select a product to add to cart")
            return
        
        # Get product details
        values = self.product_tree.item(selected_item[0], "values")
        product_id = values[0]
        name = values[2]
        price_str = values[3]
        price = float(price_str.replace("$", ""))
        
        # Get quantity
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                self.show_error("Quantity must be greater than zero")
                return
        except ValueError:
            self.show_error("Please enter a valid quantity")
            return
        
        # Check if product is already in cart
        for i, item in enumerate(self.cart_items):
            if item["product_id"] == product_id:
                # Update quantity and total
                self.cart_items[i]["quantity"] += quantity
                self.cart_items[i]["total"] = self.cart_items[i]["price"] * self.cart_items[i]["quantity"]
                
                # Update cart display
                self._update_cart_display()
                self._update_total()
                return
        
        # Add to cart
        cart_item = {
            "product_id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "total": price * quantity
        }
        self.cart_items.append(cart_item)
        
        # Update cart display
        self._update_cart_display()
        self._update_total()
    
    def _update_cart_display(self):
        """Update the cart display"""
        # Clear current items
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add cart items to treeview
        for item in self.cart_items:
            self.cart_tree.insert("", "end", values=(
                item["product_id"],
                item["name"],
                f"${item['price']:.2f}",
                item["quantity"],
                f"${item['total']:.2f}"
            ))
    
    def _update_total(self):
        """Update the total amount"""
        total = sum(item["total"] for item in self.cart_items)
        self.total_var.set(f"${total:.2f}")
    
    def _remove_from_cart(self):
        """Remove selected item from cart"""
        # Get selected item
        selected_item = self.cart_tree.selection()
        if not selected_item:
            self.show_error("Please select an item to remove")
            return
        
        # Get product ID
        product_id = self.cart_tree.item(selected_item[0], "values")[0]
        
        # Remove from cart
        self.cart_items = [item for item in self.cart_items if item["product_id"] != product_id]
        
        # Update cart display
        self._update_cart_display()
        self._update_total()
    
    def _clear_cart(self):
        """Clear the cart"""
        if self.cart_items and self.confirm("Are you sure you want to clear the cart?"):
            self.cart_items = []
            self._update_cart_display()
            self._update_total()
    
    def _checkout(self):
        """Process checkout"""
        if not self.cart_items:
            self.show_error("Cart is empty")
            return
        
        try:
            # Create bill
            bill = self.billing_controller.create_bill(self.username, self.cart_items)
            
            # Show success message
            self.show_info(f"Bill created successfully with ID: {bill['bill_id']}")
            
            # Clear cart
            self.cart_items = []
            self._update_cart_display()
            self._update_total()
        except Exception as e:
            self.show_error(f"Error creating bill: {str(e)}")
    
    def _setup_history_tab(self, parent):
        """Set up the sales history tab
        
        Args:
            parent (widget): Parent widget
        """
        # Placeholder for sales history
        tk.Label(
            parent,
            text="Sales History",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        tk.Label(
            parent,
            text="This feature is not fully implemented in this demo.",
            bg="white"
        ).pack()
    
    def _logout(self):
        """Log out and return to login screen"""
        from views.login_view import LoginView
        self.switch_callback(LoginView) 