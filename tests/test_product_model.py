import os
import sys
import unittest
from unittest.mock import patch, mock_open
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.product_model import ProductModel

class TestProductModel(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_products_file = os.path.join(self.test_dir, "products.txt")
        
        # Create test products file
        with open(self.test_products_file, 'w') as f:
            f.write("1001,Electronics,Laptop,1200.00\n")
            f.write("1002,Electronics,Smartphone,800.00\n")
            f.write("1003,Groceries,Rice (5kg),15.50\n")
    
    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)
    
    @patch('models.product_model.os.path.join')
    def test_load_products(self, mock_join):
        # Mock the path join to return our test file
        mock_join.return_value = self.test_products_file
        
        # Create product model
        model = ProductModel()
        
        # Check if products were loaded correctly
        self.assertEqual(len(model.products_cache), 3)
        self.assertEqual(model.products_cache[0]['id'], '1001')
        self.assertEqual(model.products_cache[0]['category'], 'Electronics')
        self.assertEqual(model.products_cache[0]['name'], 'Laptop')
        self.assertEqual(model.products_cache[0]['price'], 1200.00)
    
    @patch('models.product_model.os.path.join')
    def test_get_product_by_id(self, mock_join):
        # Mock the path join to return our test file
        mock_join.return_value = self.test_products_file
        
        # Create product model
        model = ProductModel()
        
        # Test get_product_by_id
        product = model.get_product_by_id('1002')
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], 'Smartphone')
        
        # Test with non-existent ID
        product = model.get_product_by_id('9999')
        self.assertIsNone(product)
    
    @patch('models.product_model.os.path.join')
    def test_get_products_by_category(self, mock_join):
        # Mock the path join to return our test file
        mock_join.return_value = self.test_products_file
        
        # Create product model
        model = ProductModel()
        
        # Test get_products_by_category
        products = model.get_products_by_category('Electronics')
        self.assertEqual(len(products), 2)
        
        products = model.get_products_by_category('Groceries')
        self.assertEqual(len(products), 1)
        
        products = model.get_products_by_category('NonExistentCategory')
        self.assertEqual(len(products), 0)
    
    @patch('models.product_model.os.path.join')
    def test_add_product(self, mock_join):
        # Mock the path join to return our test file
        mock_join.return_value = self.test_products_file
        
        # Create product model
        model = ProductModel()
        
        # Test add_product
        product = model.add_product('1004', 'Beverages', 'Coffee', 5.99)
        self.assertEqual(product['id'], '1004')
        self.assertEqual(len(model.products_cache), 4)
        
        # Test adding duplicate product
        with self.assertRaises(ValueError):
            model.add_product('1004', 'Beverages', 'Tea', 3.99)
    
    @patch('models.product_model.os.path.join')
    def test_update_product(self, mock_join):
        # Mock the path join to return our test file
        mock_join.return_value = self.test_products_file
        
        # Create product model
        model = ProductModel()
        
        # Test update_product
        product = model.update_product('1001', name='Gaming Laptop', price=1500.00)
        self.assertEqual(product['name'], 'Gaming Laptop')
        self.assertEqual(product['price'], 1500.00)
        self.assertEqual(product['category'], 'Electronics')  # Unchanged
        
        # Test updating non-existent product
        with self.assertRaises(ValueError):
            model.update_product('9999', name='NonExistent')
    
    @patch('models.product_model.os.path.join')
    def test_delete_product(self, mock_join):
        # Mock the path join to return our test file
        mock_join.return_value = self.test_products_file
        
        # Create product model
        model = ProductModel()
        
        # Test delete_product
        result = model.delete_product('1001')
        self.assertTrue(result)
        self.assertEqual(len(model.products_cache), 2)
        self.assertIsNone(model.get_product_by_id('1001'))
        
        # Test deleting non-existent product
        with self.assertRaises(ValueError):
            model.delete_product('9999')
    
    @patch('models.product_model.os.path.join')
    def test_get_categories(self, mock_join):
        # Mock the path join to return our test file
        mock_join.return_value = self.test_products_file
        
        # Create product model
        model = ProductModel()
        
        # Test get_categories
        categories = model.get_categories()
        self.assertEqual(len(categories), 2)
        self.assertIn('Electronics', categories)
        self.assertIn('Groceries', categories)

if __name__ == '__main__':
    unittest.main() 