"""Configuration settings for the stereo processor."""

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
