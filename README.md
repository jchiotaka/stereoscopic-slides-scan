# Stereo Slide to VR Converter

Convert vintage stereoscopic slides into VR-ready format for viewing in VR headsets like Oculus. This tool automatically detects stereo pairs from mounted slides, processes them, and prepares them for VR viewing.

![Example Conversion](docs/example.jpg)

## Features

- 🎯 Automatic detection of stereo pairs from mounted slides
- 🖼️ Precise alignment and standardization of image pairs
- 🔄 Multiple image enhancement options:
  - Noise reduction (Bilateral, NLM, or Gaussian)
  - Dust and scratch removal
  - Aging artifact correction
- 🕶️ VR-ready output format
- 🔍 Debug mode for viewing processing steps
- 🌐 Built-in VR viewer for immediate viewing in Oculus Browser

## Installation

1. Clone the repository:


2. Install requirements:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Processing

Convert a single slide:
```bash
python stereo_processor/main.py input_slide.jpg output_vr.jpg
```

### Enhanced Processing

With noise reduction:
```bash
python stereo_processor/main.py input_slide.jpg output_vr.jpg --noise-reduction bilateral --noise-strength medium
```

Full processing:
```bash
python stereo_processor/main.py input_slide.jpg output_vr.jpg --remove-dust --remove-aging --noise-reduction bilateral
```

### Available Options

| Option | Values | Description |
|--------|--------|-------------|
| `--noise-reduction` | `bilateral`, `nlm`, `gaussian` | Noise reduction method |
| `--noise-strength` | `low`, `medium`, `high` | Intensity of noise reduction |
| `--remove-dust` | flag | Remove dust and scratches |
| `--remove-aging` | flag | Correct aging artifacts |
| `--debug` | flag | Save debug images |

## Viewing in VR

### Quick Start
1. Process your slide
2. Start the viewer:
```bash
cd viewer
python serve.py
```
3. Open Oculus Browser
4. Navigate to the displayed IP address
5. Click for fullscreen mode

### Detailed Viewing Instructions

1. Ensure your computer and Oculus are on the same network
2. Run the viewer server:
```bash
cd viewer
python serve.py
```
3. Note the IP address displayed in the console
4. In your Oculus:
   - Open Oculus Browser
   - Navigate to `http://<displayed-ip>:8000`
   - Click anywhere on the page to enter fullscreen mode
   - Position the headset for comfortable viewing

## Project Structure

```
stereo-vr-converter/
├── stereo_processor/    # Main processing modules
│   ├── processors/      # Image processing components
│   └── utils/          # Utility functions
├── viewer/             # VR viewing components
└── docs/              # Documentation
```

## Processing Pipeline

1. **Mount Detection**: Automatically identifies and extracts stereo pairs
2. **Image Enhancement**: Applies selected processing options
3. **VR Formatting**: Prepares images for VR viewing
4. **Viewing**: Serves processed images for VR viewing

## Troubleshooting

### Common Issues

1. **Mount Detection Fails**
   - Ensure slide is well-lit and properly scanned
   - Use debug mode to view detection steps

2. **Viewer Not Accessible**
   - Verify computer and Oculus are on same network
   - Check firewall settings for port 8000

3. **Image Enhancement Issues**
   - Try different noise reduction methods
   - Adjust strength settings
   - Use debug mode to view intermediate results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Clone the repository
2. Install development requirements:
```bash
pip install -e ".[dev]"
```
3. Run tests:
```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original slide mount detection algorithm inspired by vintage photo processing techniques
- Noise reduction methods based on OpenCV implementations
- Thanks to the vintage photography community for testing and feedback

## Contact

For bugs, questions, or suggestions, please [open an issue](https://github.com/yourusername/stereo-vr-converter/issues).
