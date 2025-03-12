# app.py

# Import Global Packages
from flask import Flask, request, send_file, jsonify
from io import BytesIO
import cv2
import numpy as np
from flask_cors import CORS

# Import Weather Effect Libraries
from lib.dehaze.dehaze import *
from lib.derain.rain_model import *

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Say Hello
@app.route('/', methods=['GET'])
def sayHello():
    return jsonify("Hello, I'm flask server.")


# Dehaze
@app.route('/haze', methods=['POST'])
def dehaze_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Read the image
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Remove haze
    dehazer = ImageDehazer()
    dehazed_image = dehazer.dehaze(image)

    print("Image processing completed successfully!")

    # Save the processed image to a byte stream
    _, img_encoded = cv2.imencode('.png', dehazed_image)
    img_bytes = BytesIO(img_encoded.tobytes())

    # Return the processed image with matrics
    response = send_file(img_bytes, mimetype='image/png')

    return response, 200


# DeRain
@app.route('/rain', methods=['POST'])
def derain_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Read the image
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Initialize the model
    derainer = RainRemovalModel(model_path="lib/derain/model_deraining.pth")

    # Remove rain from the image
    derained_image = derainer.remove_rain(image)

    print("Image processing completed successfully!")

    # Save the processed image to a byte stream
    _, img_encoded = cv2.imencode('.png', derained_image)
    img_bytes = BytesIO(img_encoded.tobytes())

    # Return the processed image with matrics
    response = send_file(img_bytes, mimetype='image/png')

    return response, 200


# Custom 404 error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Path not found"}), 404
