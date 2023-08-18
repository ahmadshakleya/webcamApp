from flask import Flask, request, send_from_directory, jsonify
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'C:\Users\a98009562\OneDrive - ONEVIRTUALOFFICE\Desktop\cameraTest'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.form.get('imageData')
    if image_data:
        image_data = base64.b64decode(image_data.split(',')[1])
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'photo.png')
        with open(filename, 'wb') as f:
            f.write(image_data)
        return jsonify(message='Photo uploaded successfully')
    return jsonify(error='No image data received')

@app.route('/photos')
def photos():
    photos = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.png'):
            photos.append(filename)
    return jsonify(photos=photos)

@app.route('/photos/<filename>')
def get_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Add a route to serve photos for downloading
@app.route('/download/<filename>')
def download_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
