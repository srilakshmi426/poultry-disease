from flask import Flask, render_template, request, send_from_directory, url_for
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

model = tf.keras.models.load_model('model/mobilenet_model.h5')
classes = ['Coccidiosis', 'Healthy', 'Newcastle Disease', 'Salmonella']

# Ensure folders exist
os.makedirs('uploads', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join('uploads', filename)
            file.save(filepath)

            # Preprocess image
            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Prediction
            predictions = model.predict(img_array)
            class_index = np.argmax(predictions)
            label = classes[class_index]

            return render_template('predict.html', prediction=label, filename=filename)

    return render_template('predict.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
