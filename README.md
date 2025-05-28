# Smart Mart Management System

A complete GUI-based application for managing a retail store using Python and Tkinter.

## Features

- **Admin Interface**:
  - Manage products (add, edit, delete)
  - Manage cashiers (add, edit, delete)
  - View sales reports
  - Change admin password

- **Cashier Interface**:
  - Create new bills
  - Search products
  - View sales history

## Architecture

This application follows the MVC (Model-View-Controller) pattern and N-Tier architecture:

- **Model Layer**: Handles data from text files
- **View Layer**: Tkinter GUI components
- **Controller Layer**: Business logic, validation, and flow control

## Data Storage

All data is stored in simple text files:
- `products.txt`: Stores product information
- `cashiers.txt`: Stores cashier credentials
- `admin.txt`: Stores admin credentials
- `bills.txt`: Stores bill information

## Requirements

- Python 3.6+
- Tkinter (included in standard Python installation)
- Pillow (PIL fork) for image handling

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/smart-mart.git
   ```

2. Install required packages:
   ```
   pip install pillow
   ```

3. Run the application:
   ```
   python main.py
   ```

## Default Credentials

- **Admin**:
  - Username: admin
  - Password: admin123

- **Cashier**:
  - Username: cashier1
  - Password: password123

## Building Executable

To create a standalone executable:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Build the executable:
   ```
   pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 