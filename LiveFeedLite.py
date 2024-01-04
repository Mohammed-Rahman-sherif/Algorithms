import cv2
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.io import encode_jpeg
from tensorflow.image import resize
from tensorflow.random import uniform
from tensorflow.math import abs
import threading
import time

def preprocess(frame):
    try:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except cv2.error:
        img = uniform([250, 250, 3], minval=0, maxval=256)
    img = resize(img, (100, 100))
    img = img / 255.0
    return img

# Load the quantized model using TensorFlow Lite Interpreter
interpreter = tf.lite.Interpreter(model_path='quantized_model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

binary_cross_loss = BinaryCrossentropy()

print("Input should be one among the following ['ps_lights', 'ps_fe', 'ps_grid', 'ps_pe', 'ps_four', 'ps_top', 'dashboard', 'dup', 'layout', 'grid', 'two']")
val_img_type = input("Input Here: ")  # Set your desired category here
val_img_path = f"multi_classes_images/{val_img_type}/"

# Open the camera
cap = cv2.VideoCapture(0)

# Set a lower resolution for faster processing
cap.set(3, 640)
cap.set(4, 480)

cap.set(cv2.CAP_PROP_FPS, 30)
start_time = time.time()
frames_processed = 0

def process_frames():
    global frames_processed
    while True:
        ret, frame = cap.read()
        results = []
        for path in os.listdir(val_img_path):
            val_path = f"multi_classes_images/{val_img_type}/{path}"
            val_image = cv2.imread(val_path)
            
            # Preprocess the images
            input_img = preprocess(frame)
            val_img = preprocess(val_image)

            # Concatenate the two images along a new axis
            input_tensor = np.concatenate([input_img, val_img], axis=-1)
            input_tensor = np.expand_dims(input_tensor, axis=0)

            # Ensure that the third dimension of the input tensor has the correct size
            expected_input_size = input_details[0]['shape'][3]
            current_input_size = input_tensor.shape[3]
            
            if current_input_size != expected_input_size:
                # Resize the third dimension to match the expected size
                input_tensor = np.resize(input_tensor, (1, 100, 100, expected_input_size))

            # Set input tensor
            interpreter.set_tensor(input_details[0]['index'], input_tensor)

            # Run inference
            interpreter.invoke()

            # Get the output
            result = interpreter.get_tensor(output_details[0]['index'])

            print(result)

            if result >= 0.4:
                print(f"{val_img_type} switch component is not defective")
                results.append('Not Defective')
            else:
                print(f"{val_img_type} switch component is defective")
                results.append('Defective')

        print(results)
        label = "Not Defective" if results.count("Not Defective") > results.count("Defective") else "Defective"
        print(f"Prediction for {val_img_type} category: {label}")
        cv2.putText(frame, f"{val_img_type} - {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Calculate and display FPS
        frames_processed += 1
        elapsed_time = time.time() - start_time
        fps = frames_processed / elapsed_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Defect Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Start a separate thread for processing frames
thread = threading.Thread(target=process_frames)
thread.start()

# Wait for the thread to finish
thread.join()

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
