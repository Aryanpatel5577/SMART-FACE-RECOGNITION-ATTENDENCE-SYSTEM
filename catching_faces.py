# ==========================================
# STEP 1: Import Required Libraries
# ==========================================
import cv2        # OpenCV library for computer vision and webcam access
import pickle     # Library to save/load Python objects to files (.pkl)
import numpy as np # Library for numerical operations and array manipulation
import os         # Library to interact with the operating system (folder/file checks)


# ==========================================
# STEP 2: Initialize Webcam & Model
# ==========================================
# Start the default webcam (0 is usually the built-in laptop camera)
video = cv2.VideoCapture(0)

# Load the Haar Cascade pre-trained model for detecting frontal faces
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')


# ==========================================
# STEP 3: Setup Variables & User Input
# ==========================================
# Empty list to store cropped face images
faces_data = []

# Frame counter to help control sample collection rate
i = 0

# Ask user to enter their name in the console
name = input("Enter Your Name: ")


# ==========================================
# STEP 4: Live Webcam Capture Loop
# ==========================================
while True:
    # Read a single frame from the webcam (ret = True/False, frame = image array)
    ret, frame = video.read()
    
    # Convert the colored frame to grayscale (face detection works better in grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale image (returns list of bounding boxes: x, y, width, height)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    # Loop through each detected face in the frame
    for (x, y, w, h) in faces:
        # Crop only the face region from the original color frame
        crop_img = frame[y:y+h, x:x+w, :]
        
        # Resize the cropped face image to a standard 50x50 pixels size
        resized_img = cv2.resize(crop_img, (50, 50))
        
        # Save every 10th frame until we collect 100 face images
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
            
        i = i + 1
        
        # Draw the count of collected face images on the screen (top-left)
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        
        # Draw a red rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
        
    # Display the live webcam frame in a window titled "Frame"
    cv2.imshow("Frame", frame)
    
    # Wait for 1 millisecond for a key press
    k = cv2.waitKey(1)
    
    # Break out of loop if user presses 'q' or if 100 face samples are collected
    if k == ord('q') or len(faces_data) == 100:
        break

# Release the camera hardware and close all OpenCV window popups
video.release()
cv2.destroyAllWindows()


# ==========================================
# STEP 5: Process Captured Face Data
# ==========================================
# Convert collected faces list into a NumPy array
faces_data = np.asarray(faces_data)

# Flatten each 50x50x3 image into a 1D array of size 7500 for model training
faces_data = faces_data.reshape(100, -1)


# ==========================================
# STEP 6: Save or Update Names in 'names.pkl'
# ==========================================
if 'names.pkl' not in os.listdir('data/'):
    # If file doesn't exist, create a list repeating the name 100 times and save it
    names = [name] * 100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    # If file exists, load existing names, append the new name 100 times, and save back
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    names = names + [name] * 100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)


# ==========================================
# STEP 7: Save or Update Faces in 'faces_data.pkl'
# ==========================================
if 'faces_data.pkl' not in os.listdir('data/'):
    # If file doesn't exist, save the new face data array
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    # If file exists, load old face array, append new face array to it, and save back
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)