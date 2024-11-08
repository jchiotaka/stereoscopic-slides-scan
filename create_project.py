import os

def create_directory_structure():
    """Create the project directory structure."""
    directories = [
        "utils",
        "processors",
        "tests"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Create __init__.py in each directory
        with open(os.path.join(directory, "__init__.py"), "w") as f:
            if "utils" in directory:
                f.write("from .image_loader import ImageLoader\nfrom .image_saver import ImageSaver\n")
            elif "processors" in directory:
                f.write("from .mount_detector import MountDetector\nfrom .vr_converter import VRConverter\n")
            else:
                f.write("")

def write_file(filepath, content):
    """Write content to a file."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

# File contents
requirements_txt = """numpy>=1.21.0
opencv-python>=4.5.0
Pillow>=8.0.0
pytest>=7.0.0  # for testing
"""

config_py = '''"""Configuration settings for the stereo processor."""

# VR output settings
VR_WIDTH = 2160  # Oculus Rift resolution per eye
VR_HEIGHT = 1200

# Mount detection settings
MIN_WINDOW_AREA = 1000  # Minimum area for a valid window
ASPECT_RATIO_RANGE = (0.8, 1.2)  # Expected range for window aspect ratio

# Image enhancement settings
CLAHE_CLIP_LIMIT = 2.0
CLAHE_GRID_SIZE = (8, 8)

# Debug settings
DEBUG_MODE = True
DEBUG_OUTPUT_DIR = "debug_output"
'''

image_loader_py = '''"""Utility functions for loading and validating images."""

import os
import cv2
import numpy as np
from typing import Tuple, Optional

class ImageLoader:
    @staticmethod
    def validate_path(image_path: str) -> bool:
        """
        Validate if the image path exists and is a file.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            bool: True if path is valid, False otherwise
        """
        return os.path.isfile(image_path)
    
    @staticmethod
    def load_image(image_path: str) -> Optional[np.ndarray]:
        """
        Load an image file and perform basic validation.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            np.ndarray: Loaded image if successful, None otherwise
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image couldn't be loaded or is invalid
        """
        if not ImageLoader.validate_path(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")
            
        return image
    
    @staticmethod
    def get_image_info(image: np.ndarray) -> Tuple[int, int, int]:
        """
        Get basic information about the loaded image.
        
        Args:
            image: Loaded image array
            
        Returns:
            Tuple[int, int, int]: Height, width, and number of channels
        """
        height, width = image.shape[:2]
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        return height, width, channels
'''

image_saver_py = '''"""Utility functions for saving processed images and debug output."""

import os
import cv2
import numpy as np
from datetime import datetime
from typing import Optional

class ImageSaver:
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the ImageSaver with an output directory.
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def _generate_filename(self, prefix: str, suffix: str) -> str:
        """Generate a unique filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}{suffix}"
    
    def save_image(self, 
                  image: np.ndarray, 
                  filename: str,
                  create_debug: bool = False) -> Optional[str]:
        """
        Save an image file with optional debug version.
        
        Args:
            image: Image array to save
            filename: Desired filename
            create_debug: Whether to save a copy in debug directory
            
        Returns:
            str: Path to saved file if successful, None otherwise
        """
        try:
            # Ensure file has proper extension
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename += '.jpg'
                
            filepath = os.path.join(self.output_dir, filename)
            success = cv2.imwrite(filepath, image)
            
            if not success:
                raise ValueError(f"Failed to save image: {filepath}")
                
            # Save debug copy if requested
            if create_debug:
                debug_dir = os.path.join(self.output_dir, "debug")
                if not os.path.exists(debug_dir):
                    os.makedirs(debug_dir)
                    
                debug_filename = self._generate_filename("debug", os.path.splitext(filename)[1])
                debug_filepath = os.path.join(debug_dir, debug_filename)
                cv2.imwrite(debug_filepath, image)
                
            return filepath
            
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return None
    
    def save_debug_image(self, 
                        image: np.ndarray,
                        description: str) -> Optional[str]:
        """
        Save a debug image with description.
        
        Args:
            image: Debug image to save
            description: Short description of the debug image
            
        Returns:
            str: Path to saved debug file if successful, None otherwise
        """
        debug_dir = os.path.join(self.output_dir, "debug")
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
            
        filename = self._generate_filename(f"debug_{description}", ".jpg")
        filepath = os.path.join(debug_dir, filename)
        
        try:
            success = cv2.imwrite(filepath, image)
            if not success:
                raise ValueError(f"Failed to save debug image: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving debug image: {str(e)}")
            return None
'''

def main():
    # Create directory structure
    create_directory_structure()
    
    # Write files
    write_file("requirements.txt", requirements_txt)
    write_file("config.py", config_py)
    write_file("utils/image_loader.py", image_loader_py)
    write_file("utils/image_saver.py", image_saver_py)
    
    print("Project structure created successfully!")
    print("\nTo get started:")
    print("1. cd stereo_processor")
    print("2. pip install -r requirements.txt")

if __name__ == "__main__":
    main()