import os
from pathlib import Path

class ProductModel:
    def __init__(self):
        self.products_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "products.txt")
        self.products_cache = []
        self.load_products()
    
    def load_products(self):
        """Load all products from the products.txt file"""
        try:
            self.products_cache = []
            if os.path.exists(self.products_file):
                with open(self.products_file, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line:  # Skip empty lines
                            parts = line.split(',')
                            if len(parts) >= 4:
                                product = {
                                    'id': parts[0],
                                    'category': parts[1],
                                    'name': parts[2],
                                    'price': float(parts[3])
                                }
                                self.products_cache.append(product)
        except Exception as e:
            print(f"Error loading products: {e}")
    
    def get_all_products(self):
        """Get all products"""
        return self.products_cache
    
    def get_product_by_id(self, product_id):
        """Get a product by ID"""
        for product in self.products_cache:
            if product['id'] == product_id:
                return product
        return None
    
    def get_products_by_category(self, category):
        """Get all products in a specific category"""
        return [product for product in self.products_cache if product['category'] == category]
    
    def add_product(self, product_id, category, name, price):
        """Add a new product"""
        # Check if product with this ID already exists
        if self.get_product_by_id(product_id) is not None:
            raise ValueError(f"Product with ID {product_id} already exists")
        
        # Add to cache
        product = {
            'id': product_id,
            'category': category,
            'name': name,
            'price': float(price)
        }
        self.products_cache.append(product)
        
        # Save to file
        self._save_products()
        
        return product
    
    def update_product(self, product_id, category=None, name=None, price=None):
        """Update an existing product"""
        product = self.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")
        
        # Update fields
        if category is not None:
            product['category'] = category
        if name is not None:
            product['name'] = name
        if price is not None:
            product['price'] = float(price)
        
        # Save to file
        self._save_products()
        
        return product
    
    def delete_product(self, product_id):
        """Delete a product"""
        product = self.get_product_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} not found")
        
        # Remove from cache
        self.products_cache.remove(product)
        
        # Save to file
        self._save_products()
        
        return True
    
    def get_categories(self):
        """Get list of unique categories"""
        categories = set()
        for product in self.products_cache:
            categories.add(product['category'])
        return sorted(list(categories))
        
    def _save_products(self):
        """Save all products to the products.txt file"""
        try:
            with open(self.products_file, 'w') as file:
                for product in self.products_cache:
                    file.write(f"{product['id']},{product['category']},{product['name']},{product['price']:.2f}\n")
        except Exception as e:
            print(f"Error saving products: {e}") 