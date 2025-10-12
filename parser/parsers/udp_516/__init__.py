import sys
import os

# Get the absolute path to the directory of this __init__.py file
current_package_dir = os.path.dirname(os.path.abspath(__file__))

# Add this directory to the beginning of sys.path
# This makes all modules within this package directly discoverable by name which is necessary 
# for auto-generated files that might use flat imports to find each other or other siblings.
if current_package_dir not in sys.path:
    sys.path.insert(0, current_package_dir)