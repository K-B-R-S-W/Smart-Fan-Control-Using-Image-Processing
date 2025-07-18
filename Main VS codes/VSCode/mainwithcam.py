import os
import cv2
import numpy as np
import tensorflow as tf
import math
import requests
import time

# Ensure TensorFlow uses only the GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Set TensorFlow to only use the first GPU
        tf.config.set_visible_devices(gpus[1], 'GPU')
        # Optional: Enable memory growth to prevent TensorFlow from allocating all GPU memory at once
        tf.config.experimental.set_memory_growth(gpus[1], True)
        print("TensorFlow is using the GPU.")
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
else:
    print("No GPU detected. TensorFlow will default to CPU.")

# Load the model and labels
model_path = r"C:\Users\DEATHSEC\Desktop\TCC2\keras_model.h5"
labels_path = r"C:\Users\DEATHSEC\Desktop\TCC2\labels.txt"
model = tf.keras.models.load_model(model_path)

with open(labels_path, 'r') as file:
    labels = file.read().splitlines()

# ESP32 connection details
ESP32_IP = "http://172.20.10.2"
print(f"ESP32 IP set to: {ESP32_IP}")

def check_esp32_connection(esp32_ip):
    print("Checking ESP32 connection...")
    while True:
        try:
            response = requests.get(f"{esp32_ip}/fanoff")
            if response.status_code == 200:
                print("ESP32 connection established.")
                return True
        except requests.exceptions.ConnectionError:
            print("Waiting for ESP32. Retrying in 2 seconds...")
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(2)

# Open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not found.")
    exit()

print("Camera successfully opened. Starting detection...")

# Hand detector initialization
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300

fan_speed_level = 0
previous_command = None 
request_cooldown = 5  
last_request_time = 0 

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture image.")
        break

    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        
        if (y - offset < 0) or (x - offset < 0) or (y + h + offset > img.shape[0]) or (x + w + offset > img.shape[1]):
            print("Warning: Hand region out of bounds. Adjust offset or hand position.")
            continue

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        aspectRatio = h / w
        if (aspectRatio > 1):
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize

        imgWhite = cv2.resize(imgWhite, (224, 224))
        imgWhite = np.expand_dims(imgWhite, axis=0) / 255.0

        prediction = model.predict(imgWhite)
        index = np.argmax(prediction)
        label = labels[index]
        print(f"Prediction: {label}")

        new_command = None  
        current_time = time.time()  

        try:
            if label == '0 Paper':  
                fan_speed_level = 3
                new_command = "fanlevel3"
            elif label == '1 Rock': 
                fan_speed_level = 0
                new_command = "fanoff"
            elif label == '3 Thumbs_up':  
                fan_speed_level = 1
                new_command = "fanon"
            elif label == '2 Scissors':  
                if fan_speed_level > 1 and (current_time - last_request_time) >= request_cooldown:
                    fan_speed_level -= 1
                    new_command = "fanspeeddown"
                    last_request_time = current_time  
            elif label == '4 Up': 
                if fan_speed_level < 3 and (current_time - last_request_time) >= request_cooldown:
                    fan_speed_level += 1
                    new_command = "fanspeedup"
                    last_request_time = current_time 

            if new_command and new_command != previous_command:
                requests.get(f"{ESP32_IP}/{new_command}")
                print(f"Sent command to ESP32: {new_command.capitalize()}")
                previous_command = new_command 

        except requests.exceptions.ConnectionError as e:
            print(f"Error sending command to ESP32: {e}")
            print("Rechecking ESP32 connection...")
            check_esp32_connection(ESP32_IP)
            continue

        cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 90, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, label, (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)
        
        imgDisplay = np.uint8(imgWhite[0] * 255)
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgDisplay)

    cv2.imshow("Image", imgOutput)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quit signal received. Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
print("Camera released and all OpenCV windows closed.")

try:
    requests.get(f"{ESP32_IP}/off")
    print("Sent command to ESP32: All Off")
except requests.exceptions.ConnectionError as e:
    print(f"Error sending 'off' command to ESP32: {e}")
