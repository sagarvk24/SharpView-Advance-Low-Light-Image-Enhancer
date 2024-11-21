import sys
from PIL import Image

def convert_to_ppm(input_file, output_file, target_resolution=(1920, 1080)):
    # Open the image using Pillow
    with Image.open(input_file) as img:
        # Print the original resolution
        print(f"Original resolution: {img.size}")

        # Check if the image is larger than the target resolution
        if img.size[0] > target_resolution[0] or img.size[1] > target_resolution[1]:
            # Resize the image while maintaining the aspect ratio
            img.thumbnail(target_resolution, Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality downsampling
            print(f"Resized to: {img.size}")

        # Convert and save to PPM format
        img.save(output_file, format='PPM')
        print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    # Specify input and output file paths
    input_file = sys.argv[1]   # Input image file path (JPEG/PNG)
    output_file = "image.ppm" 
    # Define the target resolution for resizing (e.g., 1920x1080)
    target_resolution = (1920, 1080)  # Full HD resolution for faster processing
    
    # Convert to PPM after resizing
    convert_to_ppm(input_file, output_file, target_resolution)
    
    print(input_file)
