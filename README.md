# Property Image Enhancer

## Overview

Property Image Enhancer is an AI-powered image processing tool designed to prepare property images for real estate listings.

The application automatically:

* Detects and removes people from property images
* Removes clutter and temporary objects
* Cleans visible floor dirt and debris
* Enhances image brightness and clarity
* Improves overall visual quality
* Preserves the original architecture and room layout

The solution uses:

* YOLOv8 Segmentation for person detection
* OpenAI GPT Image Editing for intelligent object removal and enhancement
* OpenCV for mask processing
* Pillow for image handling

---

## Features

### Person Removal

Automatically detects people using YOLOv8 segmentation and creates masks for removal.

### Clutter Cleanup

Removes temporary objects such as:

* Trash
* Cardboard boxes
* Packaging materials
* Cleaning tools
* Loose movable items

### Property Preservation

Preserves:

* Doors
* Windows
* Walls
* Ceilings
* Floors
* Cabinets
* Shelves
* AC Units
* Fixtures
* Room Layout

### Image Enhancement

Improves:

* Brightness
* Sharpness
* Clarity
* Color Accuracy
* Lighting Balance

### Property Listing Ready Output

Generates professional-quality images suitable for:

* Real Estate Listings
* Property Portals
* Commercial Property Marketing
* Rental Listings

---

## Project Structure

```text
image-enhancer-gptapi/
│
├── input/
│   ├── 1_input.JPG
│   ├── 2_input.png
│
├── output/
│
├── property_enhancer.py
├── requirements.txt
├── .env
│
├── yolov8n-seg.pt
│
└── README.md
```

---

## Requirements

### Python

```bash
Python 3.10+
```

### Dependencies

```bash
pip install -r requirements.txt
```

---

## Installation

### Clone Project

```bash
git clone <repository-url>
cd image-enhancer-gptapi
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```

---

## Download YOLO Model

Download YOLOv8 segmentation model:

```bash
yolov8n-seg.pt
```

Place it in the project root directory.

---

## Usage

Place images inside:

```text
input/
```

Run:

```bash
python property_enhancer.py input/1_input.JPG
```

Example:

```bash
python property_enhancer.py input/property.jpg
```

---

## Output

Enhanced images are saved in:

```text
output/
```

Example:

```text
output/1_input_enhanced.png
```

---

## Processing Pipeline

```text
Property Image
      │
      ▼
YOLOv8 Segmentation
      │
      ▼
Person Mask Creation
      │
      ▼
Mask Refinement
      │
      ▼
OpenAI Image Editing
      │
      ▼
Clutter Removal
      │
      ▼
Property Enhancement
      │
      ▼
Listing Ready Image
```

---

## Current Capabilities

### Supported Input Formats

* JPG
* JPEG
* PNG

### Supported Output Format

* PNG

### Automatic Tasks

* Person Removal
* Clutter Removal
* Floor Cleanup
* Brightness Enhancement
* Sharpness Enhancement
* Property Listing Optimization

---

## Known Limitations

Since GPT Image Editing is a generative AI model:

* Hidden architectural elements may occasionally be reconstructed differently
* Windows and doors partially blocked by people may vary slightly
* Furniture hidden behind people may be recreated differently
* Very large masked regions may introduce minor architectural variations

To minimize these issues:

* Smaller mask dilation is used
* Strict architecture preservation prompts are applied
* Original room geometry is preserved whenever possible

---

## Future Improvements

* SDXL Inpainting Integration
* LaMa Inpainting Integration
* Batch Image Processing
* Automatic Clutter Detection
* Floor Stain Detection
* Architecture Preservation Scoring
* Property Quality Assessment

---

Technologies Used

* Python
* OpenAI GPT Image API
* YOLOv8 Segmentation
* OpenCV
* Pillow
* NumPy
* python-dotenv


Author

Developed as a Property Listing Enhancement Solution for real estate image preparation and automated property photo cleanup.