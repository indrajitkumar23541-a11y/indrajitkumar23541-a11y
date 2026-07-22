from PIL import Image

def trim_dark_borders(im, threshold=15):
    # Convert to grayscale
    gray = im.convert("L")
    # Create a mask where pixels > threshold are 255 (white), else 0 (black)
    mask = gray.point(lambda p: 255 if p > threshold else 0)
    bbox = mask.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

print("Opening image...")
img = Image.open('assets/banner2.png')
print(f"Original size: {img.size}")
print("Trimming image...")
cropped = trim_dark_borders(img, threshold=15)
cropped.save('assets/banner2.png')
print(f"Cropped size: {cropped.size}")
print("Image successfully cropped and saved.")
