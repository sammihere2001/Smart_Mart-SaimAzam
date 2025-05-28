from models.user_model import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()
    
    def login_admin(self, username, password):
        """Authenticate an admin user
        
        Args:
            username (str): Admin username
            password (str): Admin password
        
        Returns:
            bool: True if authentication is successful, False otherwise
        """
        if not username or not password:
            return False
        
        return self.user_model.authenticate_admin(username, password)
    
    def login_cashier(self, username, password):
        """Authenticate a cashier user
        
        Args:
            username (str): Cashier username
            password (str): Cashier password
        
        Returns:
            bool: True if authentication is successful, False otherwise
        """
        if not username or not password:
            return False
        
        return self.user_model.authenticate_cashier(username, password)
    
    def get_all_cashiers(self):
        """Get all cashiers
        
        Returns:
            list: List of cashiers
        """
        return self.user_model.get_all_cashiers()
    
    def add_cashier(self, username, password, confirm_password):
        """Add a new cashier
        
        Args:
            username (str): New cashier username
            password (str): New cashier password
            confirm_password (str): Confirm password
            
        Returns:
            bool: True if cashier was added successfully
            
        Raises:
            ValueError: If validation fails or cashier already exists
        """
        # Validate input
        if not username:
            raise ValueError("Username is required")
        
        if not password or not confirm_password:
            raise ValueError("Password is required")
        
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long")
        
        # Add cashier
        return self.user_model.add_cashier(username, password)
    
    def update_cashier_password(self, username, new_password, confirm_password):
        """Update cashier password
        
        Args:
            username (str): Cashier username
            new_password (str): New password
            confirm_password (str): Confirm password
            
        Returns:
            bool: True if password was updated successfully
            
        Raises:
            ValueError: If validation fails or cashier not found
        """
        # Validate input
        if not new_password or not confirm_password:
            raise ValueError("Password is required")
        
        if new_password != confirm_password:
            raise ValueError("Passwords do not match")
        
        if len(new_password) < 4:
            raise ValueError("Password must be at least 4 characters long")
        
        # Update password
        return self.user_model.update_cashier_password(username, new_password)
    
    def delete_cashier(self, username):
        """Delete a cashier
        
        Args:
            username (str): Cashier username
            
        Returns:
            bool: True if cashier was deleted successfully
            
        Raises:
            ValueError: If cashier not found
        """
        return self.user_model.delete_cashier(username)
    
    def update_admin_password(self, username, current_password, new_password, confirm_password):
        """Update admin password
        
        Args:
            username (str): Admin username
            current_password (str): Current password
            new_password (str): New password
            confirm_password (str): Confirm password
            
        Returns:
            bool: True if password was updated successfully
            
        Raises:
            ValueError: If validation fails or admin not found or current password is incorrect
        """
        # Validate input
        if not self.login_admin(username, current_password):
            raise ValueError("Current password is incorrect")
        
        if not new_password or not confirm_password:
            raise ValueError("New password is required")
        
        if new_password != confirm_password:
            raise ValueError("Passwords do not match")
        
        if len(new_password) < 4:
            raise ValueError("Password must be at least 4 characters long")
        
        # Update password
        return self.user_model.update_admin_password(username, new_password)
    
    def login(self, username, password):
        """Login a user
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            str: User type ("admin" or "cashier")
            
        Raises:
            ValueError: If login fails
        """
        if not username or not password:
            raise ValueError("Please enter both username and password")
            
        # Try admin login
        if self.login_admin(username, password):
            return "admin"
            
        # Try cashier login
        if self.login_cashier(username, password):
            return "cashier"
            
        raise ValueError("Invalid username or password") 