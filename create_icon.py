# ShamaOllama Icon Creation
# This script creates a simple icon for the application

from PIL import Image, ImageDraw, ImageFont
import os


def create_shamollama_icon():
    """Create a simple icon for ShamaOllama"""

    # Create a 64x64 image with a dark background
    size = 64
    img = Image.new("RGBA", (size, size), (45, 45, 55, 255))  # Dark blue-gray
    draw = ImageDraw.Draw(img)

    # Draw a guitar-like shape to represent music/rock theme
    # Body of guitar (circle)
    center = size // 2
    radius = 20

    # Guitar body - main circle
    draw.ellipse(
        [center - radius, center - radius + 5, center + radius, center + radius + 5],
        fill=(70, 130, 180, 255),
        outline=(100, 160, 210, 255),
        width=2,
    )

    # Guitar neck
    neck_width = 4
    neck_height = 25
    draw.rectangle(
        [
            center - neck_width // 2,
            center - radius - neck_height,
            center + neck_width // 2,
            center - radius,
        ],
        fill=(139, 69, 19, 255),
    )  # Brown

    # Guitar head
    draw.ellipse(
        [
            center - 6,
            center - radius - neck_height - 8,
            center + 6,
            center - radius - neck_height + 2,
        ],
        fill=(139, 69, 19, 255),
    )

    # Sound hole
    draw.ellipse(
        [center - 8, center - 3, center + 8, center + 13], fill=(20, 20, 30, 255)
    )

    # Strings
    for i in range(3):
        y_pos = center - radius - neck_height + (i + 1) * 6
        draw.line(
            [center - 1, y_pos, center - 1, center + radius],
            fill=(220, 220, 220, 180),
            width=1,
        )
        draw.line(
            [center + 1, y_pos, center + 1, center + radius],
            fill=(220, 220, 220, 180),
            width=1,
        )

    # Add "S" for ShamaOllama in a small corner
    try:
        # Try to load a font, fall back to default if not available
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    draw.text((size - 15, 5), "S", fill=(255, 255, 255, 255), font=font)

    # Save as ICO file
    img.save(
        "shamollama_icon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )

    # Also save as PNG for other uses
    img.save("shamollama_icon.png", format="PNG")

    print("✅ Icon created: shamollama_icon.ico")
    print("✅ Icon created: shamollama_icon.png")


if __name__ == "__main__":
    try:
        create_shamollama_icon()
    except ImportError:
        print("❌ PIL (Pillow) not available. Installing...")
        os.system("pip install Pillow")
        try:
            create_shamollama_icon()
        except Exception as e:
            print(f"❌ Could not create icon: {e}")
            print("💡 You can manually create an icon file named 'shamollama_icon.ico'")
