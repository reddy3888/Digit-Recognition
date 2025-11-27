import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

# Load the model
MODEL_PATH = 'mnist_model.h5'
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print(f"Model file not found at {MODEL_PATH}. Please run train_model.py first.")

load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        # Try loading again in case it was just trained
        load_model()
        if model is None:
            return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500

    try:
        data = request.get_json()
        image_data = data['image']
        
        # Decode base64 image
        # Remove the header "data:image/png;base64,"
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Preprocess image
        # Convert to grayscale
        image = image.convert('L')
        
        # Smart preprocessing to match MNIST format
        # 1. Get bounding box of the drawn digit
        bbox = image.getbbox()
        
        if bbox:
            # 2. Crop the digit
            digit = image.crop(bbox)
            
            # 3. Resize to fit in 20x20 box while maintaining aspect ratio
            width, height = digit.size
            max_dim = max(width, height)
            
            if max_dim > 0:
                scale = 20.0 / max_dim
                new_width = int(width * scale)
                new_height = int(height * scale)
                
                digit = digit.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 4. Create a new 28x28 black image
                new_image = Image.new('L', (28, 28), 0)
                
                # 5. Paste the resized digit in the center (center of mass would be better, but geometric center is good enough)
                paste_x = (28 - new_width) // 2
                paste_y = (28 - new_height) // 2
                new_image.paste(digit, (paste_x, paste_y))
                
                image = new_image
        else:
            # Empty canvas
            image = image.resize((28, 28))
        
        # Convert to numpy array
        img_array = np.array(image)
        
        # Invert colors (MNIST is white on black, canvas is usually black on white or vice versa)
        # Our canvas will be black drawing on white background, so we need to invert?
        # Actually, let's check how we draw.
        # If we draw black on white, we need to invert because MNIST is white digits on black background.
        # If we draw white on black, we don't need to invert.
        # Let's assume we draw white on black in the frontend for consistency with MNIST.
        
        # Normalize
        img_array = img_array / 255.0
        
        # Reshape
        img_array = img_array.reshape(1, 28, 28, 1)
        
        # Predict
        prediction = model.predict(img_array)
        predicted_digit = np.argmax(prediction)
        confidence = float(np.max(prediction))
        
        return jsonify({
            'digit': int(predicted_digit),
            'confidence': confidence
        })

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
