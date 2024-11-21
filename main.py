# from flask import Flask, request, jsonify, send_from_directory, make_response
# from flask_cors import CORS
# import os
# import subprocess
# import glob
# import time  # Import time for unique filenames

# app = Flask(__name__, static_folder="Frontend")
# CORS(app)

# # Define upload and enhanced folders
# UPLOAD_FOLDER = 'uploads'
# ENHANCED_FOLDER = r'E:\Minor 1\Application\enhanced'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['ENHANCED_FOLDER'] = ENHANCED_FOLDER

# # Ensure the upload and enhanced directories exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(ENHANCED_FOLDER, exist_ok=True)

# # Route for serving the index.html page
# @app.route('/')
# def serve_index():
#     return send_from_directory('Frontend', 'index.html')


# # Serve files from the static folder as needed
# @app.route('/static/<path:filename>')
# def serve_frontend(filename):
#     return send_from_directory('static', filename)

# # Route to handle static files, including CSS
# @app.route('/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('Frontend', filename)

# # Disable caching for enhanced images by adding cache control headers
# @app.route('/images/<filename>')
# def serve_image(filename):
#     response = make_response(send_from_directory(ENHANCED_FOLDER, filename))
#     response.headers['Cache-Control'] = 'no-store'  # Prevent caching of images
#     return response

# # New route to serve all images
# @app.route('/images', methods=['GET'])
# def get_all_images():
#     all_images = []
    
#     # Get images from the uploads folder
#     upload_images = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
#     for img in upload_images:
#         all_images.append(f'/uploads/{os.path.basename(img)}')

#     # Get images from the enhanced folder
#     enhanced_images = glob.glob(os.path.join(app.config['ENHANCED_FOLDER'], '*'))
#     for img in enhanced_images:
#         all_images.append(f'/enhanced/{os.path.basename(img)}')

#     return jsonify(success=True, images=all_images)

# def clear_enhanced_folder():
#     # Remove all files in the enhanced folder before each enhancement process
#     files = glob.glob(os.path.join(app.config['ENHANCED_FOLDER'], '*'))
#     for file in files:
#         os.remove(file)

# @app.route('/enhance', methods=['POST'])
# def enhance_image():
#     clear_enhanced_folder()
    
#     if 'image' not in request.files:
#         return jsonify(success=False, message="No image part")
    
#     file = request.files['image']
#     if file.filename == '':
#         return jsonify(success=False, message="No selected file")
    
#     input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#     file.save(input_image_path)

#     try:
#         # Use the full path to the Python executable
#         subprocess.run([r"E:\Minor 1\Application\myenv\Scripts\python.exe", 'automation.py', input_image_path], check=True)

#         # Rename the enhanced images with a unique identifier
#         timestamp = str(int(time.time()))
#         enhanced_images = glob.glob(os.path.join(ENHANCED_FOLDER, '*'))
#         unique_enhanced_images = []
#         for img_path in enhanced_images:
#             new_filename = f"{timestamp}_{os.path.basename(img_path)}"
#             new_path = os.path.join(ENHANCED_FOLDER, new_filename)
#             os.rename(img_path, new_path)
#             unique_enhanced_images.append(f'/images/{new_filename}')

#         if not unique_enhanced_images:
#             return jsonify(success=False, message="No enhanced images found.")

#         return jsonify(success=True, images=unique_enhanced_images)

#     except subprocess.CalledProcessError as e:
#         return jsonify(success=False, message="Image enhancement failed", error=str(e))
#     except Exception as e:
#         return jsonify(success=False, message="An unexpected error occurred", error=str(e))
    

# @app.route('/iterative_enhance', methods=['GET'])
# def iterative_enhance():
#     brightness = request.args.get('brightness', default=0, type=float)
#     input_image_path = r"E:\Minor 1\Application\output_gamma.ppm"
#     output_image_path = r"E:\Minor 1\Application\iterative_enhanced_output.ppm"
#     jpeg_output_path = r"E:\Minor 1\Application\enhanced\iterative_enhanced_output.jpg"
    
#     try:
#         # First, enhance the image
#         subprocess.run([
#             r"E:\Minor 1\Application\myenv\Scripts\python.exe", 
#             "iterativeEnhance.py", 
#             str(brightness), 
#             "1.2",  # Fixed contrast factor
#             input_image_path, 
#             output_image_path
#         ], check=True)

#         # Then, convert the enhanced PPM image to JPEG using imageBackward.py
#         # subprocess.run([
#         #     r"E:\Minor 1\Application\myenv\Scripts\python.exe", 
#         #     "imageBackward.py"
#         # ], check=True)  # No need to pass paths as they are hardcoded in imageBackward.py
               
#         # # After conversion, the path is saved in path.txt
#         # with open(r"E:\Minor 1\Application\Frontend\path.txt", 'r') as f:
#         #     jpeg_image_path = f.read().strip()
        
        
#         # Return the unique path to the image
#         # unique_image_path = f"/images/{os.path.basename(jpeg_image_path)}"
#         return jsonify(success=True, image=r"E:\Minor 1\Application\enhanced\iterative_enhanced_output.jpg")

#     except subprocess.CalledProcessError as e:
#         return jsonify(success=False, message="Enhancement or conversion failed", error=str(e))


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
