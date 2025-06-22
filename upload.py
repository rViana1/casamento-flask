from flask import Flask, render_template, request
import os
from uuid import uuid4

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')
    count = 0
    fotos_path = os.path.join(app.config['UPLOAD_FOLDER'], 'fotos')
    videos_path = os.path.join(app.config['UPLOAD_FOLDER'], 'videos')
    os.makedirs(fotos_path, exist_ok=True)
    os.makedirs(videos_path, exist_ok=True)
    for file in files:
        if file.filename != '':
            mimetype = file.mimetype
            ext = os.path.splitext(file.filename)[1]
            unique_name = f"{uuid4().hex}{ext}"
            if mimetype.startswith('image/'):
                file.save(os.path.join(fotos_path, unique_name))
                count += 1
            elif mimetype.startswith('video/'):
                file.save(os.path.join(videos_path, unique_name))
                count += 1
    return render_template('upload.html', num_files=count)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)