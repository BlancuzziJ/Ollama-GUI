# Convert PNG icon to ICO format for Windows shortcuts
# This ensures compatibility with Windows desktop shortcuts

try:
    from PIL import Image
    import os
    
    # Path to the existing PNG icon
    png_path = os.path.join("assets", "images", "icons", "ShamaOllama_Icon.png")
    ico_path = os.path.join("assets", "images", "icons", "ShamaOllama_Icon.ico")
    
    if os.path.exists(png_path):
        # Open the PNG image
        img = Image.open(png_path)
        
        # Convert to ICO with multiple sizes for Windows
        img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128)])
        
        print(f"✅ Successfully converted {png_path} to {ico_path}")
        print("🎯 ICO file created for Windows desktop shortcuts")
    else:
        print(f"❌ PNG file not found: {png_path}")
        
except ImportError:
    print("❌ PIL (Pillow) not installed. Installing...")
    os.system("pip install Pillow")
    print("🔄 Please run this script again after installation.")
except Exception as e:
    print(f"❌ Error converting icon: {e}")
