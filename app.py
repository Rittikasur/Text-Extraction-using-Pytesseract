from flask import Flask
from flask_restful import Api, Resource, reqparse
import pytesseract
import cv2
import os
from flask import Flask, request, flash, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def text_extract():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "No file selected"
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename),0)
    thresh2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 199, 5)
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'#'/usr/share/tesseract-ocr/4.00/tessdata'
    text = pytesseract.image_to_string(thresh2)
    prediction = {'text':text}

    return jsonify(prediction)

if __name__ == '__main__':   
    app.run(debug=True, port='8081')