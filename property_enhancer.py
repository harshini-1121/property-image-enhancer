import os
import cv2
import base64
import numpy as np

from pathlib import Path
from PIL import Image

from dotenv import load_dotenv
from ultralytics import YOLO
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

model = YOLO("yolov8n-seg.pt")

REMOVE_CLASSES = [
    0,   # person
]
PROMPT = """
PROPERTY LISTING ENHANCEMENT

OBJECTIVE:
Create a clean, professional property listing image while preserving the original property exactly.

REMOVE ONLY:
- people
- trash
- clutter
- cardboard boxes
- packaging materials
- cleaning tools
- temporary objects
- loose movable items

STRICT PRESERVATION RULES:

Edit ONLY the masked regions.

Everything outside the mask must remain unchanged.

Preserve exactly:
- room layout
- building structure
- walls
- ceilings
- floors
- doors
- windows
- grills
- railings
- balconies
- AC units
- cabinets
- shelves
- machinery
- industrial equipment
- fixtures
- electrical points
- switches
- lighting fixtures
- signage

DO NOT:
- redesign the property
- create new architecture
- create new furniture
- create new appliances
- create new cabinets
- create new shelves
- add AC units
- remove AC units
- add windows
- remove windows
- add doors
- remove doors
- change room dimensions
- change perspective
- change camera position
- change cabinet size
- change shelf size
- extend furniture
- modify visible architecture

FLOOR CLEANING:
Remove dirt, stains, debris, dust and clutter while preserving the original flooring material, pattern, texture and color.

IMAGE ENHANCEMENT:
Improve:
- brightness
- lighting balance
- sharpness
- clarity
- color accuracy

The final image must be the SAME property photograph with only clutter removed and image quality improved.

Preserve exact geometry, exact architecture, exact fixtures and exact proportions.
"""
# -----------------------------
# IMAGE PREP
# -----------------------------

def convert_to_jpeg(image_path):

    img = Image.open(image_path)

    if img.mode != "RGB":
        img = img.convert("RGB")

    converted_path = "temp_input.jpg"

    img.save(
        converted_path,
        format="JPEG",
        quality=95
    )

    return converted_path

# -----------------------------
# MASK CREATION
# -----------------------------

def create_mask(image_path):

    results = model(image_path)

    image = cv2.imread(image_path)

    h, w = image.shape[:2]

    mask = np.zeros(
        (h, w),
        dtype=np.uint8
    )

    for r in results:

        if r.masks is None:
            continue

        for i, seg in enumerate(r.masks.xy):

            cls = int(r.boxes.cls[i])

            if cls in REMOVE_CLASSES:

                pts = np.array(
                    seg,
                    dtype=np.int32
                )

                cv2.fillPoly(
                    mask,
                    [pts],
                    255
                )

    kernel = np.ones(
        (5,5),
        np.uint8
    )

    mask = cv2.dilate(
        mask,
        kernel,
        iterations=1
    )

    mask = Image.fromarray(mask)

    mask = mask.convert("RGBA")

    mask_path = "temp_mask.png"

    mask.save(mask_path)

    return mask_path

# -----------------------------
# OPENAI EDIT
# -----------------------------

def edit_image(image_path, mask_path):

    with open(image_path, "rb") as image_file, \
         open(mask_path, "rb") as mask_file:

        response = client.images.edit(
            model="gpt-image-1",
            image=image_file,
            mask=mask_file,
            prompt=PROMPT
        )

    return response.data[0].b64_json

# -----------------------------
# SAVE OUTPUT
# -----------------------------

def save_output(image_b64, original_file):

    os.makedirs(
        "output",
        exist_ok=True
    )

    output_file = (
        f"output/{Path(original_file).stem}_enhanced.png"
    )

    with open("temp_output.png", "wb") as f:

        f.write(
            base64.b64decode(image_b64)
        )

    original_img = Image.open(original_file)
    original_size = original_img.size

    generated_img = Image.open("temp_output.png")

    generated_img = generated_img.resize(
        original_size,
        resample=Image.LANCZOS
    )
    generated_img.save(output_file)
    os.remove("temp_output.png")

    return output_file

# -----------------------------
# MAIN
# -----------------------------

def process_image(image_path):

    print("\nConverting image...")

    converted = convert_to_jpeg(
        image_path
    )

    print("Creating mask...")

    mask = create_mask(
        converted
    )

    print("Sending to OpenAI...")

    image_b64 = edit_image(
        converted,
        mask
    )

    output_file = save_output(
        image_b64,
        image_path
    )

    saved_img = Image.open(output_file)

    print(f"\nSaved: {output_file}")
    print(f"Output Size: {saved_img.size}")


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:

        print(
            "Usage:\n"
            "python property_enhancer.py input/image.jpg"
        )

        exit()

    process_image(
        sys.argv[1]
    )

if os.path.exists("temp_input.jpg"):
    os.remove("temp_input.jpg")

if os.path.exists("temp_mask.png"):
    os.remove("temp_mask.png")