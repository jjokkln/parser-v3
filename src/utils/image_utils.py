import os
import shutil
from pathlib import Path

def get_image_path(image_name, use_static=False):
    """
    Get the path to an image, with an option to use the static directory for HTTP/HTTPS serving
    
    Args:
        image_name: The name of the image file (e.g., 'galdoralogo.png')
        use_static: If True, use the static/images path for HTTPS compatibility
        
    Returns:
        str: The path to the image file
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define paths
    sources_dir = os.path.join(project_root, 'sources')
    static_dir = os.path.join(project_root, 'static', 'images')
    
    # Ensure static/images directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
    
    # Source file path
    source_path = os.path.join(sources_dir, image_name)
    
    # If using static path for HTTPS
    if use_static:
        static_path = os.path.join(static_dir, image_name)
        
        # Copy the file to static directory if it doesn't exist there
        if os.path.exists(source_path) and not os.path.exists(static_path):
            shutil.copy2(source_path, static_path)
            
        return static_path
    
    # Otherwise return the original path
    return source_path

def ensure_images_in_static():
    """
    Copy all images from sources directory to static/images directory 
    to ensure they are available for HTTPS serving
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define paths
    sources_dir = os.path.join(project_root, 'sources')
    static_dir = os.path.join(project_root, 'static', 'images')
    
    # Ensure static/images directory exists
    if not os.path.exists(static_dir):
        os.makedirs(static_dir, exist_ok=True)
    
    # Copy all image files from sources to static/images
    for file in os.listdir(sources_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            source_file = os.path.join(sources_dir, file)
            target_file = os.path.join(static_dir, file)
            
            # Copy file if it doesn't exist or is newer
            if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                shutil.copy2(source_file, target_file)
                
    return static_dir 