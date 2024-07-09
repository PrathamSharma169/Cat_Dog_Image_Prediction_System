from flask import Flask, request, jsonify, send_from_directory
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os
import joblib

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('cat_dog_classifier.pkl')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify(success=False, message="No image file found"), 400

    file = request.files['image']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    try:
        test_image = image.load_img(file_path, target_size=[64, 64])
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        print(result)

        prediction = 'dog' if result[0][0] == 1 else 'cat'
    except Exception as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, label=prediction)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
