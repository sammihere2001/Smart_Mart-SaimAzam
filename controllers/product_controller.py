from models.product_model import ProductModel

class ProductController:
    def __init__(self):
        self.product_model = ProductModel()
    
    def get_all_products(self):
        """Get all products
        
        Returns:
            list: List of products
        """
        return self.product_model.get_all_products()
    
    def get_product_by_id(self, product_id):
        """Get a product by ID
        
        Args:
            product_id (str): Product ID
            
        Returns:
            dict: Product dictionary or None if not found
        """
        return self.product_model.get_product_by_id(product_id)
    
    def get_products_by_category(self, category):
        """Get products by category
        
        Args:
            category (str): Product category
            
        Returns:
            list: List of products in the category
        """
        return self.product_model.get_products_by_category(category)
    
    def add_product(self, product_id, category, name, price):
        """Add a new product
        
        Args:
            product_id (str): Product ID
            category (str): Product category
            name (str): Product name
            price (str/float): Product price
            
        Returns:
            dict: The newly added product
            
        Raises:
            ValueError: If validation fails or product ID already exists
        """
        # Validate input
        if not product_id or not category or not name:
            raise ValueError("Product ID, category and name are required")
        
        try:
            price_float = float(price)
            if price_float <= 0:
                raise ValueError("Price must be greater than zero")
        except ValueError:
            raise ValueError("Price must be a valid number")
        
        # Add product
        return self.product_model.add_product(product_id, category, name, price_float)
    
    def update_product(self, product_id, category=None, name=None, price=None):
        """Update a product
        
        Args:
            product_id (str): Product ID
            category (str, optional): Product category
            name (str, optional): Product name
            price (str/float, optional): Product price
            
        Returns:
            dict: The updated product
            
        Raises:
            ValueError: If validation fails or product not found
        """
        # Check if product exists
        if not self.get_product_by_id(product_id):
            raise ValueError(f"Product with ID {product_id} not found")
        
        # Validate price if provided
        if price is not None:
            try:
                price_float = float(price)
                if price_float <= 0:
                    raise ValueError("Price must be greater than zero")
            except ValueError:
                raise ValueError("Price must be a valid number")
        else:
            price_float = None
        
        # Update product
        return self.product_model.update_product(product_id, category, name, price_float)
    
    def delete_product(self, product_id):
        """Delete a product
        
        Args:
            product_id (str): Product ID
            
        Returns:
            bool: True if product was deleted successfully
            
        Raises:
            ValueError: If product not found
        """
        return self.product_model.delete_product(product_id)
    
    def get_categories(self):
        """Get list of unique categories
        
        Returns:
            list: List of categories
        """
        return self.product_model.get_categories()
    
    def search_products(self, search_term):
        """Search products by ID, name or category
        
        Args:
            search_term (str): Search term
            
        Returns:
            list: List of products matching the search term
        """
        search_term = search_term.lower()
        products = self.get_all_products()
        
        results = []
        for product in products:
            if (search_term in product['id'].lower() or 
                search_term in product['name'].lower() or 
                search_term in product['category'].lower()):
                results.append(product)
                
        return results 