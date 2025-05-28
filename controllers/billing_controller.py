import uuid
from datetime import datetime
import json
from models.bill_model import BillModel
from models.product_model import ProductModel
from controllers.sales_controller import SalesController

class BillingController:
    def __init__(self):
        self.bill_model = BillModel()
        self.product_model = ProductModel()
        self.sales_controller = SalesController()
    
    def create_bill(self, cashier, cart_items):
        """Create a new bill
        
        Args:
            cashier (str): Cashier username
            cart_items (list): List of items in the cart [{"product_id": id, "quantity": qty}, ...]
            
        Returns:
            dict: The newly created bill
            
        Raises:
            ValueError: If validation fails
        """
        # Validate input
        if not cashier:
            raise ValueError("Cashier name is required")
        
        if not cart_items:
            raise ValueError("Cart cannot be empty")
        
        # Process items
        bill_items = []
        total_amount = 0
        
        for item in cart_items:
            product_id = item['product_id']
            quantity = int(item['quantity'])
            
            if quantity <= 0:
                raise ValueError(f"Quantity must be greater than zero for product {product_id}")
            
            product = self.product_model.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} not found")
            
            item_total = product['price'] * quantity
            bill_items.append({
                'product_id': product_id,
                'name': product['name'],
                'category': product['category'],
                'price': product['price'],
                'quantity': quantity,
                'total': item_total
            })
            
            total_amount += item_total
        
        # Generate bill ID
        bill_id = str(uuid.uuid4())[:8]
        
        # Create bill
        bill = self.bill_model.add_bill(bill_id, cashier, bill_items, total_amount)
        
        # Save sales data
        with open(self.sales_controller.sales_file, "r+") as f:
            sales = json.load(f)
            sales.append({
                "date": datetime.now().isoformat(),
                "bill_id": bill_id,
                "cashier": cashier,
                "items": bill_items,
                "total": total_amount
            })
            f.seek(0)
            json.dump(sales, f, indent=2)
            f.truncate()
        
        return bill
    
    def get_all_bills(self):
        """Get all bills
        
        Returns:
            list: List of bills
        """
        return self.bill_model.get_all_bills()
    
    def get_bill_by_id(self, bill_id):
        """Get a bill by ID
        
        Args:
            bill_id (str): Bill ID
            
        Returns:
            dict: Bill dictionary or None if not found
        """
        return self.bill_model.get_bill_by_id(bill_id)
    
    def get_bills_by_date_range(self, start_date, end_date):
        """Get bills in a date range
        
        Args:
            start_date (str): Start date in format YYYY-MM-DD
            end_date (str): End date in format YYYY-MM-DD
            
        Returns:
            list: List of bills in the date range
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            return self.bill_model.get_bills_by_date_range(start_date, end_date)
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD")
    
    def get_bills_by_cashier(self, cashier):
        """Get bills by cashier
        
        Args:
            cashier (str): Cashier username
            
        Returns:
            list: List of bills by the cashier
        """
        return self.bill_model.get_bills_by_cashier(cashier)
    
    def calculate_total_sales(self, bills):
        """Calculate total sales from a list of bills
        
        Args:
            bills (list): List of bills
            
        Returns:
            float: Total sales amount
        """
        return sum(bill['total_amount'] for bill in bills) 