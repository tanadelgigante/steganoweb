from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import encode and decode functions using the environment variable path
import sys
sys.path.append(os.path.dirname(os.getenv('MAIN_PY_PATH', '/app/main.py')))
from main import encode, decode

app = Flask(__name__)
# Configure CORS to accept requests from both external and internal addresses
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://web-app:3000",  # Usa il nome del container
            "http://192.168.188.120:60"  # Indirizzo IP
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/encode', methods=['POST'])
def encode_image():
    logger.debug("Encode endpoint called")
    try:
        data = request.json
        logger.debug(f"Received data keys: {data.keys()}")
        
        if 'image' not in data or 'message' not in data:
            logger.error("Missing required fields")
            return jsonify({'error': 'Missing image or message'}), 400

        image_data = base64.b64decode(data['image'].split(',')[1])
        message = data['message']
        
        # Create a copy of the input image in memory
        input_image = io.BytesIO(image_data)
        output_image = io.BytesIO()
        
        logger.debug("Opening image with PIL")
        img = Image.open(input_image)
        img_copy = img.copy()  # Create a copy to work with
        
        logger.debug(f"Image format: {img.format}, size: {img.size}, mode: {img.mode}")
        logger.debug("Calling encode function")
        
        # Pass the image object directly, not as a path
        encode(img_copy, output_image, message)
        
        output_image.seek(0)
        encoded_image = base64.b64encode(output_image.getvalue()).decode()
        
        return jsonify({'image': f'data:image/png;base64,{encoded_image}'})
    except Exception as e:
        logger.exception("Error in encode_image:")
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