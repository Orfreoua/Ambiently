from flask import Flask, jsonify, request
from epub2txt import epub2txt
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Flask App!"


@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello, World!',
        'status': 'success'
    }
    return jsonify(data)


@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    response = {
        'message': 'Data received',
        'data': data
    }
    return jsonify(response), 201


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path


@app.route('/run', methods=['POST'])
def run():
    '''
    From: https://pypi.org/project/epub2txt/
    '''
    data = request.get_json()
    epub_file_path = data['epub_file_path']
    chapter_list = epub2txt(epub_file_path, outputlist=True)
    print(chapter_list[1])


if __name__ == '__main__':
    app.run(debug=True)
