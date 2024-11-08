"""Component for converting stereo pairs to VR-ready format."""

import cv2
import numpy as np
from typing import Tuple

class VRConverter:
    def __init__(self, target_width: int = 2160, target_height: int = 1200):
        """
        Initialize the VR converter.
        
        Args:
            target_width: Width of each eye's view in pixels
            target_height: Height of each eye's view in pixels
        """
        self.target_width = target_width
        self.target_height = target_height

    def resize_for_vr(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image to match VR display dimensions.
        
        Args:
            image: Input image
            
        Returns:
            np.ndarray: Resized image
        """
        return cv2.resize(image, (self.target_width, self.target_height))

    def apply_barrel_distortion(self, 
                              image: np.ndarray, 
                              strength: float = 0.6) -> np.ndarray:
        """
        Apply barrel distortion correction for VR viewing.
        
        Args:
            image: Input image
            strength: Distortion strength (0.0 to 1.0)
            
        Returns:
            np.ndarray: Distortion-corrected image
        """
        rows, cols = image.shape[:2]
        center_x = cols / 2
        center_y = rows / 2
        
        # Create coordinate maps
        y, x = np.mgrid[0:rows, 0:cols]
        x = x.astype(np.float32) - center_x
        y = y.astype(np.float32) - center_y
        
        # Calculate radius and normalized coordinates
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)
        
        # Apply distortion
        r_distorted = r * (1 + strength * (r / center_x)**2)
        
        # Convert back to Cartesian coordinates
        x_distorted = center_x + r_distorted * np.cos(theta)
        y_distorted = center_y + r_distorted * np.sin(theta)
        
        # Remap image
        return cv2.remap(
            image,
            x_distorted.astype(np.float32),
            y_distorted.astype(np.float32),
            cv2.INTER_LINEAR
        )

    def create_vr_image(self, 
                       left_image: np.ndarray, 
                       right_image: np.ndarray,
                       apply_distortion: bool = True) -> np.ndarray:
        """
        Create VR-ready image from stereo pair.
        
        Args:
            left_image: Left eye image
            right_image: Right eye image
            apply_distortion: Whether to apply barrel distortion
            
        Returns:
            np.ndarray: VR-ready image
        """
        # Resize images
        left_vr = self.resize_for_vr(left_image)
        right_vr = self.resize_for_vr(right_image)
        
        # Apply barrel distortion if requested
        if apply_distortion:
            left_vr = self.apply_barrel_distortion(left_vr)
            right_vr = self.apply_barrel_distortion(right_vr)
        
        # Combine images side by side
        return np.hstack((left_vr, right_vr))
