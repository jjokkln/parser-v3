import os
import shutil
import streamlit as st
from pathlib import Path

def get_image_path(image_name, use_static=True):
    """
    Get the path to an image, with an option to use the static directory for HTTP/HTTPS serving
    
    Args:
        image_name: The name of the image file (e.g., 'galdoralogo.png')
        use_static: If True, use the static/images path for HTTPS compatibility (default: True)
        
    Returns:
        str: The path to the image file
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define paths
    sources_dir = os.path.join(project_root, 'sources')
    static_dir = os.path.join(project_root, 'static', 'images')
    
    # Detect if we're running in Streamlit Cloud
    is_streamlit_cloud = os.environ.get('STREAMLIT_SHARING_MODE') == 'streamlit' or \
                          os.environ.get('IS_STREAMLIT_CLOUD') == 'true'
    
    # Always use static for Streamlit Cloud and when explicitly requested
    use_static = use_static or is_streamlit_cloud
    
    # Ensure static/images directory exists
    if not os.path.exists(static_dir):
        try:
            os.makedirs(static_dir, exist_ok=True)
            print(f"Created static directory: {static_dir}")
        except Exception as e:
            print(f"Error creating static directory: {e}")
    
    # If using static path for HTTPS (always in deployed environments)
    if use_static:
        # First, try the static path
        static_path = os.path.join(static_dir, image_name)
        
        # If the image doesn't exist in static, try to copy it from sources
        if not os.path.exists(static_path) and os.path.exists(sources_dir):
            source_path = os.path.join(sources_dir, image_name)
            if os.path.exists(source_path):
                try:
                    shutil.copy2(source_path, static_path)
                    print(f"Copied image from {source_path} to {static_path}")
                except Exception as e:
                    print(f"Error copying image: {e}")
        
        # Check if the static image exists now
        if os.path.exists(static_path):
            return static_path
        
        # If we're in Streamlit Cloud and image is still not found, try relative path
        if is_streamlit_cloud:
            for potential_path in [
                f"./static/images/{image_name}",
                f"../static/images/{image_name}",
                f"../../static/images/{image_name}",
                f"/app/static/images/{image_name}"  # Common Streamlit Cloud path
            ]:
                if os.path.exists(potential_path):
                    return potential_path
    
    # Fallback to sources dir if static wasn't used or image wasn't found
    source_path = os.path.join(sources_dir, image_name)
    if os.path.exists(source_path):
        return source_path
    
    # Final fallback: try relative paths from current directory
    for fallback_path in [
        f"./sources/{image_name}",
        f"../sources/{image_name}",
        f"./static/images/{image_name}",
        f"../static/images/{image_name}"
    ]:
        if os.path.exists(fallback_path):
            return fallback_path
    
    # If all else fails, return None instead of an invalid path
    print(f"Warning: Image {image_name} not found in any location")
    return None

def ensure_images_in_static():
    """
    Copy all images from sources directory to static/images directory 
    to ensure they are available for HTTPS serving.
    Returns the static directory path.
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Define paths
    sources_dir = os.path.join(project_root, 'sources')
    static_dir = os.path.join(project_root, 'static', 'images')
    
    # Ensure static/images directory exists
    try:
        if not os.path.exists(static_dir):
            os.makedirs(static_dir, exist_ok=True)
            print(f"Created static directory: {static_dir}")
    except Exception as e:
        print(f"Error creating static directory: {e}")
        # Try to create a relative static directory as fallback
        static_dir = "./static/images"
        try:
            os.makedirs(static_dir, exist_ok=True)
        except Exception as e2:
            print(f"Error creating fallback static directory: {e2}")
            return None
    
    # Copy all image files from sources to static/images if sources exists
    if os.path.exists(sources_dir):
        for file in os.listdir(sources_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                source_file = os.path.join(sources_dir, file)
                target_file = os.path.join(static_dir, file)
                
                try:
                    # Copy file if it doesn't exist or is newer
                    if not os.path.exists(target_file) or os.path.getmtime(source_file) > os.path.getmtime(target_file):
                        shutil.copy2(source_file, target_file)
                        print(f"Copied image from {source_file} to {target_file}")
                except Exception as e:
                    print(f"Error copying image {file}: {e}")
    else:
        print(f"Sources directory {sources_dir} not found")
    
    return static_dir

def get_image_as_bytes(image_name):
    """
    Get an image as bytes, useful for embedding in Streamlit
    
    Args:
        image_name: The name of the image file (e.g., 'galdoralogo.png')
        
    Returns:
        bytes: The image as bytes or None if not found
    """
    image_path = get_image_path(image_name, use_static=True)
    
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading image {image_name}: {e}")
    
    return None 