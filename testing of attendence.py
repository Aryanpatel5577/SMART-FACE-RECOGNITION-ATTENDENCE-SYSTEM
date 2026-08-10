import csv
import os
import pickle
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Try importing Windows Text-to-Speech library (win32com)
try:
    from win32com.client import Dispatch  # type: ignore
except ImportError:
    Dispatch = None


# Helper function to speak text aloud or fall back to printing
def speak(str1):
    if Dispatch is None:
        print(str1)
        return
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(str1)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

cascade_candidates = [
    DATA_DIR / "haarcascade.xml",
    DATA_DIR / "haarcascade_frontalface_default.xml",
]

cascade_path = next((path for path in cascade_candidates if path.exists()), None)
if cascade_path is None:
    raise FileNotFoundError(f"Could not find a Haar cascade XML file in {DATA_DIR}")

# 1. Initialize camera and verify OpenCV setup
video = cv2.VideoCapture(0)

if not hasattr(cv2, "CascadeClassifier"):
    raise AttributeError(
        "OpenCV is not installed correctly. Please reinstall opencv-python."
    )

facedetect = cv2.CascadeClassifier(str(cascade_path))

# 2. Load trained faces data and matching labels
with open("data/names.pkl", "rb") as w:
    LABELS = pickle.load(w)

with open("data/faces_data.pkl", "rb") as f:
    FACES = pickle.load(f)

print("Shape of Faces matrix --> ", FACES.shape)

# 3. Train KNN Classifier model on face data
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# 4. Load custom background image or create a fallback black image
imgBackground = cv2.imread("background.png")
if imgBackground is None:
    imgBackground = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(
        imgBackground,
        "No background image found",
        (50, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
    )

COL_NAMES = ["NAME", "TIME"]

# 5. Start main camera loop
while True:
    ret, frame = video.read()
    if not ret or frame is None:
        break

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    # Process each detected face
    for x, y, w, h in faces:
        # Crop, resize, and flatten face image for KNN prediction
        crop_img = frame[y : y + h, x : x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

        # Predict student name
        output = knn.predict(resized_img)

        # Get current date and timestamp
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

        # Draw bounding boxes and name label over face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(
            frame,
            str(output[0]),
            (x, y - 15),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 255, 255),
            1,
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

        # Prepare attendance row data
        attendance = [str(output[0]), str(timestamp)]

    # Resize camera feed and overlay it on top of the background image
    overlay_h = min(frame.shape[0], max(1, imgBackground.shape[0] - 162))
    overlay_w = min(frame.shape[1], max(1, imgBackground.shape[1] - 55))
    resized_frame = cv2.resize(frame, (overlay_w, overlay_h))
    imgBackground[162 : 162 + overlay_h, 55 : 55 + overlay_w] = resized_frame

    # Show dashboard screen
    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)

    # Press 'o' to log attendance into CSV file
    if k == ord("o"):
        speak("Attendance Taken..")
        time.sleep(5)
        if exist:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()

    # Press 'q' to quit application
    if k == ord("q"):
        break

# Release camera and clean up windows
video.release()
cv2.destroyAllWindows()
