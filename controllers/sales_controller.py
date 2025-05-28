import json
import os
from datetime import datetime, timedelta

class SalesController:
    def __init__(self):
        self.sales_file = os.path.join("data", "sales.json")
        self._ensure_sales_file_exists()
    
    def _ensure_sales_file_exists(self):
        """Ensure the sales file exists and is properly initialized"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(self.sales_file):
            with open(self.sales_file, "w") as f:
                json.dump([], f)
    
    def get_all_sales(self):
        """Get all sales records"""
        with open(self.sales_file, "r") as f:
            return json.load(f)
    
    def get_sales_by_date_range(self, start_date, end_date):
        """Get sales within a specific date range"""
        all_sales = self.get_all_sales()
        filtered_sales = [
            sale for sale in all_sales
            if start_date <= datetime.fromisoformat(sale["date"]).date() <= end_date
        ]
        return filtered_sales
    
    def get_daily_sales_summary(self, date):
        """Get sales summary for a specific day"""
        sales = self.get_sales_by_date_range(date, date)
        total_sales = sum(sale["total"] for sale in sales)
        total_items = sum(len(sale["items"]) for sale in sales)
        return {
            "date": date.isoformat(),
            "total_sales": total_sales,
            "total_transactions": len(sales),
            "total_items": total_items
        }
    
    def get_top_selling_products(self, start_date, end_date, limit=10):
        """Get top selling products within a date range"""
        sales = self.get_sales_by_date_range(start_date, end_date)
        product_sales = {}
        
        for sale in sales:
            for item in sale["items"]:
                product_id = item["product_id"]
                quantity = item["quantity"]
                if product_id in product_sales:
                    product_sales[product_id]["quantity"] += quantity
                    product_sales[product_id]["revenue"] += item["price"] * quantity
                else:
                    product_sales[product_id] = {
                        "product_name": item["name"],
                        "quantity": quantity,
                        "revenue": item["price"] * quantity
                    }
        
        # Convert to list and sort by quantity
        products_list = [
            {"product_id": k, **v}
            for k, v in product_sales.items()
        ]
        products_list.sort(key=lambda x: x["quantity"], reverse=True)
        
        return products_list[:limit]
    
    def get_sales_by_category(self, start_date, end_date):
        """Get sales summary by product category"""
        sales = self.get_sales_by_date_range(start_date, end_date)
        category_sales = {}
        
        for sale in sales:
            for item in sale["items"]:
                category = item["category"]
                if category in category_sales:
                    category_sales[category]["quantity"] += item["quantity"]
                    category_sales[category]["revenue"] += item["price"] * item["quantity"]
                else:
                    category_sales[category] = {
                        "quantity": item["quantity"],
                        "revenue": item["price"] * item["quantity"]
                    }
        
        return category_sales 