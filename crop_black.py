"""Dark border trimming utility script.

Trims dark/black letterbox margins from images using luminance thresholding.
Includes CLI argument support, Windows-safe file handles, and proper module guards.
"""

import sys
from pathlib import Path
from PIL import Image


def trim_dark_borders(im: Image.Image, threshold: int = 15) -> Image.Image:
    """Trim dark borders from an image.

    Args:
        im: PIL Image object.
        threshold: Luminance value (0-255) below which pixels are treated as black.

    Returns:
        Cropped PIL Image object, or original image if no crop bbox is found.
    """
    # Convert to grayscale luminance
    gray = im.convert("L")
    # Create binary mask where pixels > threshold are white (255), else black (0)
    mask = gray.point(lambda p: 255 if p > threshold else 0)
    bbox = mask.getbbox()
    if bbox:
        return im.crop(bbox)
    return im


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("Usage: python crop_black.py [image_path] [threshold] [output_path]")
        print("Trims pure black/dark borders from the target image.")
        return 0

    script_dir = Path(__file__).resolve().parent

    # Optional CLI arguments: python crop_black.py [image_path] [threshold] [output_path]
    image_arg = sys.argv[1] if len(sys.argv) > 1 else "assets/banner2.png"
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 15

    target_path = Path(image_arg)
    if not target_path.is_absolute():
        target_path = script_dir / target_path

    if not target_path.exists():
        print(f"Error: Image file not found: {target_path}", file=sys.stderr)
        return 1

    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else target_path
    if not output_path.is_absolute():
        output_path = script_dir / output_path

    print(f"Opening image: {target_path}")
    with Image.open(target_path) as img:
        img_loaded = img.copy()  # Release file descriptor for safe overwriting
        print(f"Original size: {img_loaded.size}")
        print(f"Trimming dark borders (threshold={threshold})...")
        cropped = trim_dark_borders(img_loaded, threshold=threshold)
        print(f"Cropped size: {cropped.size}")

        cropped.save(output_path)
        print(f"Image successfully cropped and saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
