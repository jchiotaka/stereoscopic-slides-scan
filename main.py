"""Main script for processing stereo slides to VR format."""

import argparse
from utils.image_loader import ImageLoader
from utils.image_saver import ImageSaver
from processors.mount_detector import MountDetector
from processors.noise_reducer import NoiseReducer
from processors.vr_converter import VRConverter
import config

def process_slide(
        input_path: str, 
        output_path: str, 
        debug_mode: bool = False,
        noise_reduction: str = None,
        noise_strength: str = 'medium',
        remove_dust: bool = False,
        remove_aging: bool = False):
    """
    Process a stereo slide and convert it to VR format.
    
    Args:
        input_path: Path to input slide image
        output_path: Path to save VR output
        debug_mode: Whether to save debug images
        noise_reduction: None, 'bilateral', 'nlm', or 'gaussian'
        noise_strength: 'low', 'medium', or 'high'
        remove_dust: Whether to remove dust and scratches
        remove_aging: Whether to remove aging artifacts
    """
    # Initialize components
    loader = ImageLoader()
    saver = ImageSaver(output_dir="output")
    detector = MountDetector(debug_mode=debug_mode)
    converter = VRConverter(
        target_width=config.VR_WIDTH,
        target_height=config.VR_HEIGHT
    )
    
    try:
        # Load image
        image = loader.load_image(input_path)
        
        # Extract stereo pair
        left_image, right_image = detector.extract_stereo_pair(image)
        
        # Apply restoration if requested
        if noise_reduction or remove_dust or remove_aging:
            reducer = NoiseReducer(debug_mode=debug_mode)
            left_image, right_image = reducer.process_stereo_pair(
                left_image, 
                right_image,
                remove_dust=remove_dust,
                remove_aging=remove_aging,
                denoise_method=noise_reduction if noise_reduction else 'bilateral',
                strength=noise_strength
            )
        
        # Convert to VR format
        vr_image = converter.create_vr_image(left_image, right_image)
        
        # Save result
        saver.save_image(vr_image, output_path, create_debug=debug_mode)
        
        print(f"Successfully processed {input_path}")
        print(f"Output saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing slide: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert stereo slides to VR format")
    parser.add_argument("input", help="Input slide image path")
    parser.add_argument("output", help="Output VR image path")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--noise-reduction", 
                      choices=['bilateral', 'nlm', 'gaussian'],
                      help="Noise reduction method")
    parser.add_argument("--noise-strength",
                      choices=['low', 'medium', 'high'],
                      default='medium',
                      help="Noise reduction strength")
    parser.add_argument("--remove-dust",
                      action="store_true",
                      help="Remove dust and scratches")
    parser.add_argument("--remove-aging",
                      action="store_true",
                      help="Remove aging artifacts like fading")
    
    args = parser.parse_args()
    
    # Call process_slide with keyword arguments
    process_slide(
        input_path=args.input,
        output_path=args.output,
        debug_mode=args.debug,
        noise_reduction=args.noise_reduction,
        noise_strength=args.noise_strength,
        remove_dust=args.remove_dust,
        remove_aging=args.remove_aging
    )

if __name__ == "__main__":
    main()