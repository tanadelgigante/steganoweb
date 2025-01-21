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

        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1])
        message = data['message']
        
        logger.debug(f"Message to encode: {message}")
        
        # Create input and output buffers
        input_buffer = io.BytesIO(image_data)
        output_buffer = io.BytesIO()
        
        # Open and process image
        with Image.open(input_buffer) as img:
            logger.debug(f"Image format: {img.format}, mode: {img.mode}")
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Create a copy to work with
            img_copy = img.copy()
            
            try:
                logger.debug("Calling encode function")
                # Pass the image copy directly
                encode(img_copy, output_buffer, message)
                logger.debug("Encoding completed")
            except Exception as e:
                logger.error(f"Encoding error: {str(e)}")
                raise
        
        # Prepare response
        output_buffer.seek(0)
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode()
        
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