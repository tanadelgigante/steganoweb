from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
import os
import logging
import tempfile

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
    logger.debug("=== ENCODE ENDPOINT START ===")
    try:
        data = request.json
        logger.debug(f"Message to encode: '{data.get('message')}'")
        logger.debug(f"Message length: {len(data.get('message', ''))}")
        logger.debug(f"Message bytes: {[ord(c) for c in data.get('message', '')]}")
        
        if 'image' not in data or 'message' not in data:
            logger.error("Missing required fields")
            return jsonify({'error': 'Missing image or message'}), 400

        # Extract image format from the data URL
        image_data_parts = data['image'].split(',')[0]
        image_format = image_data_parts.split(';')[0].split('/')[1].replace('jpeg', 'jpg')
        logger.debug(f"Detected image format: {image_format}")
        image_data = base64.b64decode(data['image'].split(',')[1])
        message = data['message']

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use the original format for both input and output
            input_path = os.path.join(temp_dir, f'input.{image_format}')
            output_path = os.path.join(temp_dir, f'output.{image_format}')
            
            logger.debug(f"Saving input image to {input_path}")
            # Save input image to temporary file
            with open(input_path, 'wb') as f:
                f.write(image_data)

            logger.debug(f"Calling encode with message: '{data['message']}'")
            # Call encode with file paths
            encode(input_path, output_path, message)
            logger.debug("Encode completed, now trying to decode to verify")
            
            # Verify the encoded message
            decoded = decode(output_path)
            logger.debug(f"Verification decode result: '{decoded}'")
            if decoded != data['message']:
                logger.warning(f"Encode verification failed! Original: '{data['message']}', Decoded: '{decoded}'")

            # Read output image and preserve the original format in the response
            logger.debug(f"Reading output from {output_path}")
            with open(output_path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode()
            
            return jsonify({
                'image': f'data:image/{image_format};base64,{encoded_image}'
            })

    except Exception as e:
        logger.exception("Error in encode_image:")
        return jsonify({'error': str(e)}), 400
    finally:
        logger.debug("=== ENCODE ENDPOINT END ===")

@app.route('/decode', methods=['POST'])
def decode_image():
    logger.debug("=== DECODE ENDPOINT START ===")
    try:
        data = request.json
        logger.debug(f"Received data keys: {data.keys()}")
        
        if 'image' not in data:
            logger.error("Missing image")
            return jsonify({'error': 'Missing image'}), 400

        # Extract image format and data
        image_data_parts = data['image'].split(',')[0]
        image_format = image_data_parts.split(';')[0].split('/')[1]
        logger.debug(f"Detected image format: {image_format}")
        
        image_data = base64.b64decode(data['image'].split(',')[1])

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary file path
            temp_input = os.path.join(temp_dir, f"input.{image_format}")
            
            logger.debug(f"Saving input image to {temp_input}")
            # Save input image to temporary file
            with open(temp_input, 'wb') as f:
                f.write(image_data)

            logger.debug("Starting decode operation")
            # Call decode with file path
            message = decode(temp_input)
            logger.debug(f"Decoded message: '{message}'")
            logger.debug(f"Decoded message length: {len(message)}")
            logger.debug(f"Decoded message bytes: {[ord(c) for c in message]}")

            return jsonify({'message': message})

    except Exception as e:
        logger.exception("Error in decode_image:")
        return jsonify({'error': str(e)}), 400
    finally:
        logger.debug("=== DECODE ENDPOINT END ===")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')