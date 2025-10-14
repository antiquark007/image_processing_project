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