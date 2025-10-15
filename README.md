# Image Enhancement Flowchart

```
┌────────────────────────┐
│   Start / Input Image  │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────────────┐
│  Choose Enhancement Domain      │
└────────────┬────────────────────┘
             │
┌────────────┴────────────────┐
▼                             ▼
┌──────────────────────┐    ┌─────────────────────────┐
│  SPATIAL DOMAIN      │    │  FREQUENCY DOMAIN       │
└─────────┬────────────┘    └──────────┬──────────────┘
          │                            │
          ▼                            ▼
┌──────────────────────┐       ┌──────────────────────────┐
│  Point Processing    │       │  Apply Fourier Transform │
└─────────┬────────────┘       └──────────┬──────────────┘
          │                               │
  ┌───────┴────────┐            ┌─────────┴──────────────┐
  ▼                ▼            ▼                        ▼
┌────────────┐ ┌────────────┐ ┌───────────────┐  ┌────────────────┐
│Contrast    │ │Histogram   │ │  Low-Pass     │  │  High-Pass     │
│Stretching  │ │Equalization│ │  Filtering    │  │  Filtering     │
└────────────┘ └────────────┘ └───────────────┘  └────────────────┘
     │              │              │                       │
     ▼              ▼              ▼                       ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐  ┌─────────────────┐
│Improved     │ │Uniform      │ │Smoothed     │  │Sharpened image  │
│global       │ │histogram    │ │image        │  │(edges enhanced) │
│contrast     │ │(contrast    │ │(noise       │  └─────────────────┘
└─────────────┘ │enhancement) │ │reduced)     │
                └─────────────┘ └─────────────┘
          │
          ▼
┌──────────────────────┐
│ Spatial Filtering    │
└──────────┬───────────┘
           │
  ┌────────┴─────────┐
  ▼                  ▼
┌──────────────┐   ┌───────────────┐
│Smoothing     │   │Sharpening     │
│(Mean,        │   │(Laplacian,    │
│Gaussian      │   │Unsharp mask)  │
│filters)      │   └───────────────┘
└──────────────┘          │
     │                    ▼
     ▼              ┌──────────────┐
┌─────────────┐     │Edge emphasis │
│Noise        │     └──────────────┘
│reduction    │
└─────────────┘
     │
     ▼
┌────────────┐
│Enhanced    │
│Image Output│
└────────────┘
```

## Image Enhancement Pipeline

This flowchart illustrates the **image enhancement pipeline** that starts with an input image and provides two main processing paths: **spatial domain techniques** and **frequency domain techniques** to produce an enhanced output image.

### Spatial Domain Processing
- **Point Processing**: Direct pixel manipulation
  - Contrast Stretching: Improves global contrast
  - Histogram Equalization: Uniform intensity distribution
- **Spatial Filtering**: Neighborhood-based operations
  - Smoothing: Noise reduction (Mean, Gaussian filters)
  - Sharpening: Edge enhancement (Laplacian, Unsharp masking)

### Frequency Domain Processing
- **Fourier Transform**: Convert to frequency domain
- **Low-Pass Filtering**: Smoothing and noise reduction
- **High-Pass Filtering**: Edge enhancement and sharpening

### Output
Enhanced image with improved visual quality based on the selected enhancement technique.

🧠 Explanation of Flowchart Steps
Step	Description
Input Image	Load grayscale or color image for processing.
Choose Domain	Select Spatial (pixel-based) or Frequency (Fourier-based) enhancement.
Point Processing	Operate on individual pixels: contrast stretching or histogram equalization.
Spatial Filtering	Operate on a pixel’s neighborhood: smoothing (noise removal) or sharpening (edge enhancement).
Fourier Transform	Convert image from spatial domain to frequency domain for filtering.
Low-Pass Filter	Keeps low frequencies, removes noise — gives a smooth appearance.
High-Pass Filter	Keeps high frequencies — highlights edges and fine details.
Inverse Transform	Convert back to spatial domain after frequency filtering.
Output Enhanced Image	The final improved image for visualization or analysis.


## Installation and Setup

### Prerequisites
Make sure you have Python 3.7 or higher installed on your system.

### Required Dependencies
Install the required Python packages using pip:

```bash
pip install opencv-python numpy matplotlib tkinter
```

Or install from a requirements file:

```bash
pip install -r requirements.txt
```

Create a `requirements.txt` file with the following content:
```
opencv-python>=4.5.0
numpy>=1.20.0
matplotlib>=3.3.0
```

**Note:** `tkinter` comes pre-installed with most Python distributions on Windows and macOS. On Linux, you might need to install it separately:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install tkinter
# or
sudo dnf install python3-tkinter
```

## How to Run the Project

### 1. Using Command Line
Navigate to the project directory and run:

```bash
cd a:\image_processing_project
python image_enhancement_gui.py
```

### 2. Using Python IDE
- Open `image_enhancement_gui.py` in your preferred Python IDE (VS Code, PyCharm, etc.)
- Run the script directly from the IDE

### 3. Double-click Execution (Windows)
- Ensure Python is associated with `.py` files
- Double-click on `image_enhancement_gui.py`

## Using the Application

### Getting Started
1. **Launch** the application using one of the methods above
2. **Load Image**: Click "Load Image" button and select an image file (JPG, PNG, BMP, TIFF)
3. **Apply Enhancements**: Use the various processing options in the control panel
4. **Save Results**: Click "Save Image" to export the enhanced image
5. **Reset**: Use "Reset" button to return to the original image

### Features Overview

#### Point Processing
- **Contrast Stretching**: Improves global contrast by stretching intensity range
- **Histogram Equalization**: Creates uniform intensity distribution

#### Spatial Filtering
- **Smoothing Filters**: 
  - Mean Filter: Simple averaging for noise reduction
  - Gaussian Filter: Weighted averaging with Gaussian weights
  - Median Filter: Non-linear filter for salt-and-pepper noise removal
- **Sharpening Filters**:
  - Laplacian: Edge detection and enhancement
  - Unsharp Masking: Controlled sharpening technique
  - Custom Kernel: Predefined sharpening kernel

#### Frequency Domain Filtering
- **Filter Types**: Low-pass (smoothing) and High-pass (sharpening)
- **Filter Designs**: Ideal, Butterworth, and Gaussian filters
- **Adjustable Cutoff**: Control filter frequency response

#### Analysis Tools
- **Histogram Display**: View intensity distribution
- **FFT Spectrum**: Visualize frequency domain representation

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'cv2'"
**Solution**: Install OpenCV using `pip install opencv-python`

**Issue**: "ModuleNotFoundError: No module named 'tkinter'"
**Solution**: 
- Windows/macOS: tkinter should be included with Python
- Linux: Install using system package manager (see Prerequisites section)

**Issue**: Image won't load
**Solution**: 
- Ensure the image file is not corrupted
- Check if the file format is supported
- Verify file permissions

**Issue**: Application runs slowly
**Solution**: 
- Use smaller images for testing
- Close other resource-intensive applications
- Ensure sufficient RAM is available

### Performance Tips
- For large images, processing may take longer
- Start with smaller kernel sizes for spatial filtering
- Use lower resolution images for real-time experimentation

## Project Structure
```
image_processing_project/
│
├── README.md                 # This file
├── image_enhancement_gui.py  # Main application
├── requirements.txt          # Python dependencies
└── sample_images/           # (Optional) Test images
```

## Example Workflow
1. Load a sample image
2. Try contrast stretching to improve overall appearance
3. Apply Gaussian smoothing with kernel size 5 to reduce noise
4. Use unsharp masking to enhance edges
5. Compare results using the side-by-side display
6. Save the enhanced image

---

**Note**: This application processes images in grayscale. Color images will be automatically converted to grayscale upon loading.