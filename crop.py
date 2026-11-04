"""Image trimming utility script.

Trims uniform border colors from images while safely handling file descriptors,
cross-platform path resolution, and RGBA/RGB image modes.
"""

import sys
from pathlib import Path
from PIL import Image, ImageChops


def trim(im: Image.Image, fuzz: int = 10) -> Image.Image:
    """Trim uniform border colors from an image based on top-left pixel color.

    Args:
        im: PIL Image object.
        fuzz: Color difference tolerance threshold (0-255).

    Returns:
        Cropped PIL Image object, or original image if no crop bbox is found.
    """
    bg_color = im.getpixel((0, 0))
    bg = Image.new(im.mode, im.size, bg_color)
    diff = ImageChops.difference(im, bg)

    if diff.mode in ("RGBA", "RGB", "LA"):
        diff_gray = diff.convert("L")
    else:
        diff_gray = diff

    mask = diff_gray.point(lambda p: 255 if p > fuzz else 0)
    bbox = mask.getbbox()
    if bbox:
        return im.crop(bbox)
    return im


def main() -> int:
    script_dir = Path(__file__).resolve().parent

    # Determine input path: CLI argument > assets/banner2.png > assets/banner.png
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
        if not target_path.is_absolute():
            target_path = script_dir / target_path
    else:
        candidate_paths = [
            script_dir / "assets" / "banner2.png",
            script_dir / "assets" / "banner.png",
        ]
        target_path = next((p for p in candidate_paths if p.exists()), candidate_paths[0])

    if not target_path.exists():
        print(f"Error: Target image file not found: {target_path}", file=sys.stderr)
        return 1

    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else target_path
    if not output_path.is_absolute():
        output_path = script_dir / output_path

    print(f"Opening image from: {target_path}")
    with Image.open(target_path) as img:
        img_loaded = img.copy()  # Ensure full image data loaded and handle closed
        orig_size = img_loaded.size
        print(f"Original size: {orig_size}")

        print("Trimming image...")
        cropped = trim(img_loaded)
        print(f"Cropped size: {cropped.size}")

        # Save to target destination (safe from Windows file-lock)
        cropped.save(output_path)
        print(f"Image successfully cropped and saved to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
