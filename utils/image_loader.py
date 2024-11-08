"""Utility functions for loading and validating images."""

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
