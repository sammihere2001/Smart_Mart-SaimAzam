import os
from datetime import datetime

class BillModel:
    def __init__(self):
        self.bills_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "bills.txt")
        self.bills = []
        self.load_bills()
    
    def load_bills(self):
        """Load all bills from the bills.txt file"""
        try:
            self.bills = []
            if os.path.exists(self.bills_file):
                with open(self.bills_file, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line:  # Skip empty lines
                            parts = line.split(',')
                            if len(parts) >= 5:
                                bill = {
                                    'bill_id': parts[0],
                                    'cashier': parts[1],
                                    'date': parts[2],
                                    'total_amount': float(parts[3]),
                                    'items': parts[4]  # Items are stored as a JSON string representation
                                }
                                self.bills.append(bill)
        except Exception as e:
            print(f"Error loading bills: {e}")
    
    def get_all_bills(self):
        """Get all bills"""
        return self.bills
    
    def get_bill_by_id(self, bill_id):
        """Get a bill by ID"""
        for bill in self.bills:
            if bill['bill_id'] == bill_id:
                return bill
        return None
    
    def add_bill(self, bill_id, cashier, items, total_amount):
        """Add a new bill
        
        Args:
            bill_id (str): Unique bill ID
            cashier (str): Cashier username
            items (list): List of items in the bill [{"product_id": id, "quantity": qty, "price": price}, ...]
            total_amount (float): Total bill amount
        """
        # Check if bill with this ID already exists
        if self.get_bill_by_id(bill_id) is not None:
            raise ValueError(f"Bill with ID {bill_id} already exists")
        
        # Create bill with current date
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items_str = str(items)  # Convert items list to string
        
        bill = {
            'bill_id': bill_id,
            'cashier': cashier,
            'date': date,
            'total_amount': float(total_amount),
            'items': items_str
        }
        
        # Add to cache
        self.bills.append(bill)
        
        # Save to file
        self._save_bills()
        
        return bill
    
    def get_bills_by_date_range(self, start_date, end_date):
        """Get bills in a date range
        
        Args:
            start_date (str): Start date in format YYYY-MM-DD
            end_date (str): End date in format YYYY-MM-DD
        
        Returns:
            list: List of bills in the date range
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        
        result = []
        for bill in self.bills:
            bill_date = datetime.strptime(bill['date'], "%Y-%m-%d %H:%M:%S")
            if start <= bill_date <= end:
                result.append(bill)
        
        return result
    
    def get_bills_by_cashier(self, cashier):
        """Get bills by cashier
        
        Args:
            cashier (str): Cashier username
        
        Returns:
            list: List of bills by the cashier
        """
        return [bill for bill in self.bills if bill['cashier'] == cashier]
    
    def _save_bills(self):
        """Save all bills to the bills.txt file"""
        try:
            with open(self.bills_file, 'w') as file:
                for bill in self.bills:
                    file.write(f"{bill['bill_id']},{bill['cashier']},{bill['date']},{bill['total_amount']:.2f},{bill['items']}\n")
        except Exception as e:
            print(f"Error saving bills: {e}") 