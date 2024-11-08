"""Main script for processing stereo slides to VR format."""

import argparse
from utils.image_loader import ImageLoader
from utils.image_saver import ImageSaver
from processors.mount_detector import MountDetector
from processors.vr_converter import VRConverter
import config

def process_slide(input_path: str, output_path: str, debug_mode: bool = False):
    """
    Process a stereo slide and convert it to VR format.
    
    Args:
        input_path: Path to input slide image
        output_path: Path to save VR output
        debug_mode: Whether to save debug images
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
    
    args = parser.parse_args()
    process_slide(args.input, args.output, args.debug)

if __name__ == "__main__":
    main()
