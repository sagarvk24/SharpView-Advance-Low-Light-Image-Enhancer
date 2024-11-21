import subprocess
import os
import shutil

# Define paths
UPLOADS_PATH = r"E:\Minor 1\Application\uploads"
ENHANCED_PATH = r"E:\Minor 1\Application\enhanced"
GAMMA_ENHANCER_PATH = r"E:\Minor 1\Application\GammaEnhancer.exe"
PYTHON_PATH = r"E:\Minor 1\Application\myenv\Scripts\python.exe" 

def convert_to_ppm(input_image):
    print("Converting input image to PPM format...")
    try:
        subprocess.run([PYTHON_PATH, "image.py", input_image], check=True)
        print("Conversion to PPM completed.")
    except subprocess.CalledProcessError as e:
        print("Error in PPM conversion:", e)

def run_gamma_enhancer():
    print("Running GammaEnhancer...")
    try:
        subprocess.run([GAMMA_ENHANCER_PATH], check=True)
        print("Enhancement process completed.")
    except subprocess.CalledProcessError as e:
        print("Error in GammaEnhancer execution:", e)

def convert_to_jpeg():
    print("Converting PPM images to JPEG format...")
    try:
        subprocess.run([PYTHON_PATH, "imageBackward.py"], check=True)
        print("Conversion to JPEG completed.")
    except subprocess.CalledProcessError as e:
        print("Error in JPEG conversion:", e)

def clear_uploads():
    print("Clearing uploads folder...")
    if os.path.exists(UPLOADS_PATH):
        for filename in os.listdir(UPLOADS_PATH):
            file_path = os.path.join(UPLOADS_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        print("Uploads folder cleared.")
    else:
        print("Uploads folder does not exist.")

def main(input_image):
    # Step 1: Convert input image to PPM
    convert_to_ppm(input_image)

    # Step 2: Run the image enhancement process
    run_gamma_enhancer()

    # Step 3: Convert the output PPM files to JPEG
    convert_to_jpeg()
    
    # Step 4: Clear the uploads folder
    clear_uploads()

    print("All processes completed. Enhanced images are ready for viewing.")

if __name__ == "__main__":
    # Ensure the uploads directory exists
    os.makedirs(UPLOADS_PATH, exist_ok=True)

    # Get the path of the first file in the uploads folder
    try:
        input_image_path = os.path.join(UPLOADS_PATH, os.listdir(UPLOADS_PATH)[0])
        print(f"Processing input image: {input_image_path}")
        main(input_image_path)
    except IndexError:
        print("No files found in the uploads folder.")
