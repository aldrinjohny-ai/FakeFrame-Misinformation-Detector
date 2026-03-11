"""
Utility Functions
Helper functions for file handling and validation
"""

import os
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    """
    Check if uploaded file has an allowed image extension
    Args:
        filename: Name of the uploaded file
    Returns:
        bool: True if extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(image_path):
    """
    Validate that the file is a valid image
    Args:
        image_path: Path to the image file
    Returns:
        bool: True if valid image
    """
    try:
        img = Image.open(image_path)
        img.verify()
        return True
    except Exception:
        return False

def validate_caption(caption):
    """
    Validate caption text
    Args:
        caption: Text caption string
    Returns:
        tuple: (is_valid, error_message)
    """
    if not caption or len(caption.strip()) == 0:
        return False, "Caption cannot be empty"
    
    if len(caption) > 500:
        return False, "Caption too long (max 500 characters)"
    
    return True, None

def create_directories():
    """
    Create necessary directories for the application
    """
    directories = ['uploads', 'models', 'dataset']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
