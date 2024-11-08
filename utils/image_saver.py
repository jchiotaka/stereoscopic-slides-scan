"""Utility functions for saving processed images and debug output."""

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
