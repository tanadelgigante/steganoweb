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

# Get CORS settings from environment
cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
cors_methods = os.getenv('CORS_METHODS', 'GET,POST,OPTIONS').split(',')
cors_headers = os.getenv('CORS_HEADERS', 'Content-Type').split(',')
cors_credentials = os.getenv('CORS_CREDENTIALS', 'true').lower() == 'true'
cors_max_age = int(os.getenv('CORS_MAX_AGE', 3600))

CORS(app, resources={
    r"/*": {
        "origins": cors_origins,
        "methods": cors_methods,
        "allow_headers": cors_headers,
        "supports_credentials": cors_credentials,
        "max_age": cors_max_age
    }
})

@app.route('/encode', methods=['POST'])
def encode_image():
    logger.debug("=== ENCODE ENDPOINT START ===")
    try:
        data = request.json
        message = data.get('message', '')
        logger.debug(f"Message to encode: '{message}'")
        logger.debug(f"Message length: {len(message)}")
        logger.debug(f"Message bytes: {[ord(c) for c in message]}")
        logger.debug(f"Message binary: {' '.join(format(ord(c), '08b') for c in message)}")

        # Extract image format and normalize it
        image_data_parts = data['image'].split(',')[0]
        image_format = image_data_parts.split(';')[0].split('/')[1].lower()
        if image_format == 'jpeg':
            image_format = 'jpg'
        logger.debug(f"Detected image format: {image_format}")

        image_data = base64.b64decode(data['image'].split(',')[1])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, f'input.{image_format}')
            output_path = os.path.join(temp_dir, f'output.png')  # Always save as PNG to preserve data
            
            logger.debug(f"Saving input image to {input_path}")
            with open(input_path, 'wb') as f:
                f.write(image_data)

            try:
                logger.debug(f"Calling encode with message: '{message}'")
                encode(input_path, output_path, message)
                logger.debug("Encode completed, now trying to decode to verify")
                
                # Verify encoding
                decoded = decode(output_path)
                logger.debug(f"Verification decode result: '{decoded}'")
                if decoded != message:
                    logger.warning(f"Encode verification failed! Original: '{message}', Decoded: '{decoded}'")
                    logger.debug(f"Original binary: {' '.join(format(ord(c), '08b') for c in message)}")
                    logger.debug(f"Decoded binary: {' '.join(format(ord(c), '08b') for c in decoded)}")
            
                # Read output image
                logger.debug(f"Reading output from {output_path}")
                with open(output_path, 'rb') as f:
                    output_data = f.read()
                    
                encoded_image = base64.b64encode(output_data).decode()
                return jsonify({'image': f'data:image/png;base64,{encoded_image}'})

            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                raise

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
        
        # Extract image format and normalize it
        image_data_parts = data['image'].split(',')[0]
        image_format = image_data_parts.split(';')[0].split('/')[1].lower()
        if image_format == 'jpeg':
            image_format = 'jpg'
        logger.debug(f"Detected image format: {image_format}")
        
        image_data = base64.b64decode(data['image'].split(',')[1])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, f'input.{image_format}')
            
            logger.debug(f"Saving input image to {input_path}")
            with open(input_path, 'wb') as f:
                f.write(image_data)

            logger.debug("Starting decode operation")
            message = decode(input_path)
            logger.debug(f"Decoded message: '{message}'")
            logger.debug(f"Decoded message length: {len(message)}")
            logger.debug(f"Decoded message bytes: {[ord(c) for c in message]}")
            logger.debug(f"Decoded binary: {' '.join(format(ord(c), '08b') for c in message)}")
            
            return jsonify({'message': message})

    except Exception as e:
        logger.exception("Error in decode_image:")
        return jsonify({'error': str(e)}), 400
    finally:
        logger.debug("=== DECODE ENDPOINT END ===")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')