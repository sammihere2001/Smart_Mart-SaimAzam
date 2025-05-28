import re
from datetime import datetime

def validate_id(id_str):
    """Validate an ID string
    
    Args:
        id_str (str): ID string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not id_str:
        return False
    
    # Check if ID contains only alphanumeric characters
    return bool(re.match(r'^[a-zA-Z0-9]+$', id_str))

def validate_float(value):
    """Validate a float value
    
    Args:
        value: Value to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        float_value = float(value)
        return float_value >= 0
    except (ValueError, TypeError):
        return False

def validate_int(value):
    """Validate an integer value
    
    Args:
        value: Value to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        int_value = int(value)
        return int_value >= 0
    except (ValueError, TypeError):
        return False

def validate_date_format(date_str):
    """Validate a date string in YYYY-MM-DD format
    
    Args:
        date_str (str): Date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_username(username):
    """Validate a username
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not username:
        return False
    
    # Check if username contains only letters, numbers, and underscores
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))

def validate_password(password):
    """Validate a password
    
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not password:
        return False
    
    # Check if password is at least 4 characters long
    return len(password) >= 4 