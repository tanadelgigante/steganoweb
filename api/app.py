from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
import sys
from pathlib import Path

# Import encode and decode functions from main.py
from main import encode, decode

app = Flask(__name__)
CORS(app)

@app.route('/encode', methods=['POST'])
def encode_image():
    """
    Endpoint for encoding a message into an image.
    Expects: 
    - image: base64 encoded image
    - message: text to encode
    Returns:
    - encoded image in base64 format
    """
    try:
        data = request.json
        image_data = base64.b64decode(data['image'].split(',')[1])
        message = data['message']

        # Create temporary files for processing
        input_image = io.BytesIO(image_data)
        output_image = io.BytesIO()

        # Process the image
        img = Image.open(input_image)
        encode(img, output_image, message)

        # Convert back to base64
        output_image.seek(0)
        encoded_image = base64.b64encode(output_image.getvalue()).decode()

        return jsonify({'image': f'data:image/png;base64,{encoded_image}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decode', methods=['POST'])
def decode_image():
    """
    Endpoint for decoding a message from an image.
    Expects:
    - image: base64 encoded image
    Returns:
    - decoded message
    """
    try:
        data = request.json
        image_data = base64.b64decode(data['image'].split(',')[1])

        # Create temporary file for processing
        input_image = io.BytesIO(image_data)
        img = Image.open(input_image)

        # Decode the message
        message = decode(img)

        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')