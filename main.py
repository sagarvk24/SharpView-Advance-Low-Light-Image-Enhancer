from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import os
import subprocess
import glob
from PIL import Image  # For PPM-to-JPEG conversion

app = Flask(__name__, static_folder="Frontend")
CORS(app)

# Define folders
UPLOAD_FOLDER = 'uploads'
ENHANCED_FOLDER = r'E:\Minor 1\Application\enhanced'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENHANCED_FOLDER'] = ENHANCED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

@app.route('/')
def serve_index():
    return send_from_directory('Frontend', 'index.html')

@app.route('/static/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('static', filename)

@app.route('/<path:filename>')
def serve_frontend_files(filename):
    return send_from_directory('Frontend', filename)

@app.route('/images/<filename>')
def serve_image(filename):
    response = make_response(send_from_directory(app.config['ENHANCED_FOLDER'], filename))
    response.headers['Cache-Control'] = 'no-store'  # Prevent caching of images
    return response

@app.route('/images', methods=['GET'])
def get_all_images():
    """Serve all images from uploads and enhanced folders."""
    all_images = []

    # Fetch images from uploads folder
    upload_images = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    for img in upload_images:
        all_images.append(f'/uploads/{os.path.basename(img)}')

    # Fetch images from enhanced folder
    enhanced_images = glob.glob(os.path.join(app.config['ENHANCED_FOLDER'], '*'))
    for img in enhanced_images:
        all_images.append(f'/images/{os.path.basename(img)}')

    return jsonify(success=True, images=all_images)

def clear_enhanced_folder():
    """Clear all files in the enhanced folder before each enhancement."""
    files = glob.glob(os.path.join(app.config['ENHANCED_FOLDER'], '*'))
    for file in files:
        os.remove(file)

def delete_file():
    # Specify the file path
    file_path = r"E:\Minor 1\Application\iterative_output.ppm"
    
    # Check if the file exists
    if os.path.exists(file_path):
        try:
            # Delete the file
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")
        except Exception as e:
            print(f"An error occurred while deleting the file: {e}")
    else:
        print(f"File '{file_path}' does not exist.")


@app.route('/enhance', methods=['POST'])
def enhance_image():
    delete_file()
    """Perform the initial enhancement."""
    clear_enhanced_folder()

    if 'image' not in request.files:
        return jsonify(success=False, message="No image part")
    
    file = request.files['image']
    if file.filename == '':
        return jsonify(success=False, message="No selected file")

    # Save the uploaded image
    input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(input_image_path)

    try:
        # Run the full enhancement process
        subprocess.run([
            r"E:\Minor 1\Application\myenv\Scripts\python.exe",
            'automation.py',
            input_image_path
        ], check=True)

        # Get the enhanced images (OutputGamma.jpeg, etc.)
        enhanced_images = glob.glob(os.path.join(app.config['ENHANCED_FOLDER'], '*'))
        unique_enhanced_images = [
            f'/images/{os.path.basename(img)}' for img in enhanced_images
        ]

        if not unique_enhanced_images:
            return jsonify(success=False, message="No enhanced images found.")

        return jsonify(success=True, images=unique_enhanced_images)

    except subprocess.CalledProcessError as e:
        return jsonify(success=False, message="Image enhancement failed", error=str(e))
    except Exception as e:
        return jsonify(success=False, message="An unexpected error occurred", error=str(e))
    
@app.route('/iterative_enhance', methods=['GET'])
def iterative_enhance():
    brightness = request.args.get('brightness', default=0, type=float)
    input_image_path = os.path.join(app.config['ENHANCED_FOLDER'], 'output_gamma.jpeg')
    output_ppm_path = r'E:\Minor 1\Application\iterative_output.ppm'
    output_jpeg_path = os.path.join(app.config['ENHANCED_FOLDER'], 'iterative_output.jpeg')

    try:
        subprocess.run([
            r"E:\Minor 1\Application\myenv\Scripts\python.exe",
            'iterativeEnhance.py',
            str(brightness),
            "1.0",  # Fixed contrast factor
            input_image_path,
            output_ppm_path
        ], check=True)

        Image.open(output_ppm_path).convert("RGB").save(output_jpeg_path)

        # Log for debugging
        print(f"Returning image path: {output_jpeg_path}")

        return jsonify(success=True, image=f'/images/{os.path.basename(output_jpeg_path)}')

    except Exception as e:
        return jsonify(success=False, message="Error occurred", error=str(e))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
