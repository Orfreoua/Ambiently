from flask import Flask, jsonify, request, send_from_directory
from epub2txt import epub2txt
import os
from flask_cors import CORS

app = Flask(__name__)

# Configure the directory where files will be stored
UPLOAD_FOLDER = os.path.join('back', 'uploads')  # Update folder path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS for cross-origin requests
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the "back/uploads" folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    print(f"File uploaded to {file_path}")

    # Generate a public URL
    public_url = f"http://127.0.0.1:3000/back/uploads/{file.filename}"

    return jsonify({"data": {"message": "File uploaded successfully", "url": public_url}}), 200


@app.route('/back/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    """
    Serve files from the 'back/uploads' directory.
    """
    return send_from_directory('uploads/', filename)


@app.route('/run', methods=['POST'])
def run():
    """
    Example pipeline logic for processing an EPUB file.
    """
    data = request.get_json()
    epub_file_path = data['epub_file_path']
    chapter_list = epub2txt(epub_file_path, outputlist=True)
    print(chapter_list[1])


if __name__ == '__main__':
    app.run(debug=True, port=3000)
