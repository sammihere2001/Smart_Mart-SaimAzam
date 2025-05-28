import os
import sys
import subprocess
import shutil

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        # Check if PyInstaller is installed
        subprocess.run([sys.executable, '-m', 'pip', 'show', 'pyinstaller'], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("PyInstaller is not installed. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
    
    print("Building executable...")
    
    # Clean dist and build directories if they exist
    for dir_name in ['dist', 'build']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Build the executable
    icon_path = os.path.join('assets', 'icon.ico')
    if not os.path.exists(icon_path):
        icon_option = []
        print("Warning: icon.ico not found in assets directory. Using default icon.")
    else:
        icon_option = ['--icon', icon_path]
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'SmartMart',
        '--add-data', f'assets{os.pathsep}assets',
        *icon_option,
        'main.py'
    ]
    
    result = subprocess.run(cmd, check=False)
    
    if result.returncode != 0:
        print("Error building executable.")
        return False
    
    print("Executable built successfully!")
    print(f"Executable location: {os.path.join('dist', 'SmartMart.exe')}")
    return True

if __name__ == '__main__':
    success = build_executable()
    sys.exit(0 if success else 1) 