import cv2
import numpy as np
import sys

def enhance_image(brightness, contrast, input_path, output_path):
    # Log the input path to verify it
    print(f"Reading image from: {input_path}")
    
    # Read the input image
    image = cv2.imread(input_path)
    if image is None:
        print("Failed to load the image. Check if the path is correct.")
        return
    
    # Enhance the image
    enhanced_img = np.clip(image * contrast + brightness, 0, 255).astype(np.uint8)
    
    # Save the enhanced image
    cv2.imwrite(output_path, enhanced_img)

if __name__ == "__main__":
    brightness = float(sys.argv[1])
    contrast = float(sys.argv[2])  # Explicitly convert this to float
    input_path = sys.argv[3]
    output_path = sys.argv[4]
    
    enhance_image(brightness, contrast, input_path, output_path)
