import os

class UserModel:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.admin_file = os.path.join(base_dir, "data", "admin.txt")
        self.cashiers_file = os.path.join(base_dir, "data", "cashiers.txt")
        self.admins = []
        self.cashiers = []
        self.load_users()
    
    def load_users(self):
        """Load admin and cashier users from their respective files"""
        self.admins = []
        self.cashiers = []
        
        try:
            # Load admin users
            if os.path.exists(self.admin_file):
                with open(self.admin_file, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line:  # Skip empty lines
                            parts = line.split(',')
                            if len(parts) >= 2:
                                self.admins.append({
                                    'username': parts[0],
                                    'password': parts[1]
                                })
        except Exception as e:
            print(f"Error loading admin users: {e}")
        
        try:
            # Load cashier users
            if os.path.exists(self.cashiers_file):
                with open(self.cashiers_file, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line:  # Skip empty lines
                            parts = line.split(',')
                            if len(parts) >= 2:
                                self.cashiers.append({
                                    'username': parts[0],
                                    'password': parts[1]
                                })
        except Exception as e:
            print(f"Error loading cashier users: {e}")
    
    def authenticate_admin(self, username, password):
        """Authenticate an admin user"""
        for admin in self.admins:
            if admin['username'] == username and admin['password'] == password:
                return True
        return False
    
    def authenticate_cashier(self, username, password):
        """Authenticate a cashier user"""
        for cashier in self.cashiers:
            if cashier['username'] == username and cashier['password'] == password:
                return True
        return False
    
    def get_all_cashiers(self):
        """Get all cashiers"""
        return self.cashiers
    
    def add_cashier(self, username, password):
        """Add a new cashier"""
        # Check if username already exists
        for cashier in self.cashiers:
            if cashier['username'] == username:
                raise ValueError(f"Cashier with username '{username}' already exists")
        
        # Add to cache
        cashier = {
            'username': username,
            'password': password
        }
        self.cashiers.append(cashier)
        
        # Save to file
        self._save_cashiers()
        
        return True
    
    def update_cashier_password(self, username, new_password):
        """Update cashier password"""
        for cashier in self.cashiers:
            if cashier['username'] == username:
                cashier['password'] = new_password
                self._save_cashiers()
                return True
        
        raise ValueError(f"Cashier with username '{username}' not found")
    
    def delete_cashier(self, username):
        """Delete a cashier"""
        for i, cashier in enumerate(self.cashiers):
            if cashier['username'] == username:
                del self.cashiers[i]
                self._save_cashiers()
                return True
        
        raise ValueError(f"Cashier with username '{username}' not found")
    
    def update_admin_password(self, username, new_password):
        """Update admin password"""
        for admin in self.admins:
            if admin['username'] == username:
                admin['password'] = new_password
                self._save_admins()
                return True
        
        raise ValueError(f"Admin with username '{username}' not found")
    
    def _save_admins(self):
        """Save admins to file"""
        try:
            with open(self.admin_file, 'w') as file:
                for admin in self.admins:
                    file.write(f"{admin['username']},{admin['password']}\n")
        except Exception as e:
            print(f"Error saving admin users: {e}")
    
    def _save_cashiers(self):
        """Save cashiers to file"""
        try:
            with open(self.cashiers_file, 'w') as file:
                for cashier in self.cashiers:
                    file.write(f"{cashier['username']},{cashier['password']}\n")
        except Exception as e:
            print(f"Error saving cashier users: {e}") 