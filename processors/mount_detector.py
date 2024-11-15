"""Component for detecting and extracting stereo image pairs from mounted slides."""

import cv2
import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class Window:
    x: int
    y: int
    width: int
    height: int
    image: np.ndarray

class MountDetector:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        # Constants tuned for vintage slide mounts
        self.THRESHOLD_VALUE = 200
        self.MIN_WINDOW_RATIO = 0.1
        self.MAX_WINDOW_RATIO = 0.4
        self.ASPECT_RATIO_TOL = 0.1
        # Staple removal settings
        self.STAPLE_MARGIN = 15  # Pixels to crop from edges to remove staples

    def remove_staples(self, window_image: np.ndarray) -> np.ndarray:
        """
        Remove staple marks by cropping edges of the window.
        
        Args:
            window_image: Extracted window image
            
        Returns:
            np.ndarray: Cleaned window image with staples removed
        """
        h, w = window_image.shape[:2]
        margin = self.STAPLE_MARGIN
        
        # Crop out the staple areas
        cleaned = window_image[margin:h-margin, margin:w-margin]
        
        return cleaned

    def detect_windows(self, image: np.ndarray) -> List[Window]:
        """
        Detect the two square windows in the stereo slide mount.
        Optimized for vintage stereo slides with light-colored mounts.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply strong blur to reduce noise and texture in the mount
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Use Otsu's thresholding to find a good threshold value
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Invert the image so windows are white
        binary = cv2.bitwise_not(binary)
        
        # Clean up the binary image
        kernel = np.ones((5,5), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        if self.debug_mode:
            cv2.imwrite('debug_binary.jpg', binary)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Get image dimensions for relative size calculations
        img_height, img_width = image.shape[:2]
        min_window_size = int(img_width * self.MIN_WINDOW_RATIO)
        max_window_size = int(img_width * self.MAX_WINDOW_RATIO)
        
        # Filter and sort windows
        windows = []
        for contour in contours:
            # Approximate the contour to a polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Get the rectangle bounding the contour
            x, y, w, h = cv2.boundingRect(approx)
            
            # Calculate aspect ratio and area
            aspect_ratio = w / h
            aspect_ratio_error = abs(1 - aspect_ratio)  # How far from square
            
            # Filtering criteria
            if (min_window_size < w < max_window_size and  # Width in range
                min_window_size < h < max_window_size and  # Height in range
                aspect_ratio_error < self.ASPECT_RATIO_TOL):  # Nearly square
                
                # Extract window image
                window_image = image[y:y+h, x:x+w]
                
                # Remove staples
                cleaned_image = self.remove_staples(window_image)
                
                # Update dimensions after staple removal
                h_cleaned, w_cleaned = cleaned_image.shape[:2]
                
                windows.append(Window(
                    x + self.STAPLE_MARGIN,  # Adjust coordinates for cropped margins
                    y + self.STAPLE_MARGIN,
                    w_cleaned,
                    h_cleaned,
                    cleaned_image
                ))
        
        # Sort windows left to right
        windows.sort(key=lambda w: w.x)
        
        if self.debug_mode:
            debug_img = image.copy()
            for window in windows:
                cv2.rectangle(debug_img, 
                            (window.x, window.y), 
                            (window.x + window.width, window.y + window.height), 
                            (0, 255, 0), 2)
            cv2.imwrite('debug_detection.jpg', debug_img)
        
        return windows

    def standardize_windows(self, windows: List[Window]) -> List[Window]:
        """Ensure both windows have identical dimensions."""
        if len(windows) != 2:
            raise ValueError(f"Expected 2 windows, found {len(windows)}")
        
        # Use the smaller dimension to ensure we don't exceed either window's bounds
        target_size = min(
            min(w.width for w in windows),
            min(w.height for w in windows)
        )
        
        standardized = []
        for window in windows:
            # Calculate centering offsets
            x_offset = (window.width - target_size) // 2
            y_offset = (window.height - target_size) // 2
            
            # Extract centered square region
            centered = window.image[
                y_offset:y_offset+target_size,
                x_offset:x_offset+target_size
            ]
            
            # Create new window with standardized dimensions
            standardized.append(Window(
                window.x + x_offset,
                window.y + y_offset,
                target_size,
                target_size,
                centered
            ))
            
            if self.debug_mode:
                cv2.imwrite(f'debug_window_{len(standardized)}.jpg', centered)
        
        return standardized

    def extract_stereo_pair(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Extract and standardize the stereo image pair."""
        windows = self.detect_windows(image)
        
        if len(windows) != 2:
            raise ValueError(f"Expected 2 windows, found {len(windows)}")
        
        std_windows = self.standardize_windows(windows)
        return std_windows[0].image, std_windows[1].image