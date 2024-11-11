"""Component for reducing noise, dust, and aging artifacts in vintage stereo images."""

import cv2
import numpy as np
from typing import Tuple, Optional

class NoiseReducer:
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        # Parameters for different cleaning methods
        self.BILATERAL_PARAMS = {
            'd': 9,
            'sigma_color': 75,
            'sigma_space': 75
        }
        self.NLM_PARAMS = {
            'h': 10,
            'template_window_size': 7,
            'search_window_size': 21
        }
        self.DUST_PARAMS = {
            'kernel_size': 3,
            'threshold': 30
        }
        self.MEDIAN_PARAMS = {
            'kernel_size': 3
        }

    def reduce_noise(self, 
                    image: np.ndarray, 
                    method: str = 'bilateral',
                    strength: str = 'medium') -> np.ndarray:
        """
        Apply noise reduction using specified method and strength.
        
        Args:
            image: Input image
            method: 'bilateral', 'nlm', or 'gaussian'
            strength: 'low', 'medium', or 'high'
            
        Returns:
            np.ndarray: Denoised image
        """
        # Adjust parameters based on strength
        if strength == 'low':
            self.BILATERAL_PARAMS['sigma_color'] = 50
            self.BILATERAL_PARAMS['sigma_space'] = 50
            self.NLM_PARAMS['h'] = 5
        elif strength == 'high':
            self.BILATERAL_PARAMS['sigma_color'] = 100
            self.BILATERAL_PARAMS['sigma_space'] = 100
            self.NLM_PARAMS['h'] = 15
        
        # Apply selected method
        if method == 'nlm':
            result = cv2.fastNlMeansDenoisingColored(
                image,
                None,
                h=self.NLM_PARAMS['h'],
                templateWindowSize=self.NLM_PARAMS['template_window_size'],
                searchWindowSize=self.NLM_PARAMS['search_window_size']
            )
        elif method == 'gaussian':
            kernel_size = 5 if strength == 'medium' else (3 if strength == 'low' else 7)
            result = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        else:  # bilateral
            result = cv2.bilateralFilter(
                image,
                self.BILATERAL_PARAMS['d'],
                self.BILATERAL_PARAMS['sigma_color'],
                self.BILATERAL_PARAMS['sigma_space']
            )
            
        if self.debug_mode:
            cv2.imwrite(f'debug_denoised_{method}_{strength}.jpg', result)
            
        return result

    def remove_dust_and_scratches(self, image: np.ndarray) -> np.ndarray:
        """Remove dust spots and scratches."""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Create mask for dust and scratches
        _, dust_mask = cv2.threshold(
            l, 
            self.DUST_PARAMS['threshold'], 
            255, 
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        
        # Clean up the mask
        kernel = np.ones((self.DUST_PARAMS['kernel_size'], 
                         self.DUST_PARAMS['kernel_size']), 
                         np.uint8)
        dust_mask = cv2.morphologyEx(dust_mask, cv2.MORPH_OPEN, kernel)
        
        # Apply inpainting
        cleaned = cv2.inpaint(
            image,
            dust_mask,
            3,
            cv2.INPAINT_TELEA
        )
        
        if self.debug_mode:
            cv2.imwrite('debug_dust_mask.jpg', dust_mask)
            cv2.imwrite('debug_dust_removed.jpg', cleaned)
        
        return cleaned

    def remove_aging_artifacts(self, image: np.ndarray) -> np.ndarray:
        """Remove aging artifacts like color fading."""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        # Enhance color channels
        a = cv2.convertScaleAbs(a, alpha=1.2, beta=0)
        b = cv2.convertScaleAbs(b, alpha=1.2, beta=0)
        
        # Merge channels and convert back
        enhanced_lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        if self.debug_mode:
            cv2.imwrite('debug_aging_removed.jpg', enhanced)
        
        return enhanced

    def apply_median_filter(self, image: np.ndarray) -> np.ndarray:
        """Apply median filter to remove salt-and-pepper noise."""
        return cv2.medianBlur(
            image, 
            self.MEDIAN_PARAMS['kernel_size']
        )

    def process_vintage_photo(self, 
                            image: np.ndarray,
                            remove_dust: bool = True,
                            remove_aging: bool = True,
                            denoise_method: str = 'bilateral',
                            strength: str = 'medium') -> np.ndarray:
        """Complete processing pipeline for vintage photos."""
        result = image.copy()
        
        if remove_dust:
            result = self.apply_median_filter(result)
            result = self.remove_dust_and_scratches(result)
        
        if denoise_method:
            result = self.reduce_noise(result, denoise_method, strength)
        
        if remove_aging:
            result = self.remove_aging_artifacts(result)
        
        return result

    def process_stereo_pair(self, 
                          left_image: np.ndarray, 
                          right_image: np.ndarray,
                          remove_dust: bool = True,
                          remove_aging: bool = True,
                          denoise_method: str = 'bilateral',
                          strength: str = 'medium') -> Tuple[np.ndarray, np.ndarray]:
        """Process both stereo images consistently."""
        left_processed = self.process_vintage_photo(
            left_image,
            remove_dust,
            remove_aging,
            denoise_method,
            strength
        )
        
        right_processed = self.process_vintage_photo(
            right_image,
            remove_dust,
            remove_aging,
            denoise_method,
            strength
        )
        
        return left_processed, right_processed