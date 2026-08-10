# Face Recognition Attendance System

A Python-based attendance system that uses computer vision and machine learning to recognize registered students through a webcam and record their attendance automatically.

## Overview

I built this project to explore how face detection, image processing, machine learning, and basic data management can be combined into one practical application.

The system first collects face samples for each student. These samples are processed into numerical data and stored locally. During attendance, the system uses a webcam to detect faces, compares them with the stored data using a K-Nearest Neighbors (KNN) classifier, and displays the predicted student's name. Attendance can then be recorded with the current date and time in a CSV file.

I also built a small Streamlit dashboard to view attendance records and manage registered students.

## How It Works

The project is divided into four main Python files:

### 1. `catching_faces.py`

This script is responsible for collecting training data.

* Opens the computer's webcam using OpenCV.
* Uses a Haar Cascade classifier to detect faces.
* Crops the detected face from each frame.
* Resizes each face to `50 × 50` pixels.
* Collects 100 face samples for a student.
* Converts the collected images into numerical arrays.
* Stores the face data in `faces_data.pkl`.
* Stores the corresponding student names in `names.pkl`.

The stored face data and labels are later used by the recognition module.

### 2. `testing of attendance.py`

This is the main face recognition and attendance module.

It:

* Loads the previously collected face data and student names.
* Trains a K-Nearest Neighbors classifier.
* Opens the webcam and continuously processes frames.
* Converts frames to grayscale for face detection.
* Detects faces using Haar Cascade.
* Crops and resizes detected faces to match the training format.
* Uses the KNN model to predict the student's identity.
* Displays the predicted name on the webcam feed.
* Generates the current date and timestamp.
* Records attendance in a daily CSV file when attendance is confirmed.

The recognition pipeline therefore follows:

**Webcam → Face Detection → Face Preprocessing → KNN Prediction → Attendance Record**

### 3. `data_for_student.py`

This file contains the data-management functions used by the project.

It provides functions to:

* Load registered student names.
* Load stored face data.
* List registered students.
* Add new student face samples.
* Delete a student's stored data.

Keeping these operations in a separate module makes the project easier to maintain and allows the dashboard to reuse the same functions instead of duplicating the code.

### 4. `app.py`

This file provides the Streamlit dashboard.

The dashboard can:

* Display the attendance dashboard.
* Show the current day's attendance records.
* List registered students.
* Select and delete a registered student.
* Refresh the dashboard periodically.
* Display attendance data in a table using Pandas.

The interface uses functions from `data_for_student.py`, keeping the UI and data-management logic separate.

## Technologies Used

* **Python** — Main programming language
* **OpenCV** — Webcam access, image processing, and face detection
* **Haar Cascade** — Face detection
* **NumPy** — Numerical and image-array operations
* **Scikit-learn** — K-Nearest Neighbors classifier
* **Pandas** — Reading and displaying attendance records
* **Streamlit** — Web-based dashboard
* **Pickle** — Local storage of face data and student labels
* **CSV** — Attendance record storage

## Project Structure

```text
Face-Recognition-Attendance/
│
├── catching_faces.py
├── testing of attendance.py
├── data_for_student.py
├── app.py
├── background.png
│
├── data/
│   ├── haarcascade_frontalface_default.xml
│   ├── names.pkl
│   └── faces_data.pkl
│
└── Attendance/
    └── Attendance_DD-MM-YYYY.csv
```

Some files inside `data/` and `Attendance/` are generated or updated while using the application.

## Requirements

* Python 3.x
* A working webcam
* OpenCV
* NumPy
* Scikit-learn
* Pandas
* Streamlit

Optional dependencies:

* `pywin32` — used for Windows text-to-speech
* `streamlit-autorefresh` — used for automatic dashboard refresh

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Face-Recognition-Attendance.git
cd Face-Recognition-Attendance
```

Install the required packages:

```bash
pip install opencv-python numpy scikit-learn pandas streamlit
```

For the optional features:

```bash
pip install pywin32 streamlit-autorefresh
```

## Setup

Before running the project, make sure the Haar Cascade XML file is available inside the `data` directory.

The project expects:

```text
data/
└── haarcascade_frontalface_default.xml
```

The recognition script also looks for a background image named:

```text
background.png
```

If the background image is not available, the program creates a simple fallback background instead.

## Running the Project

### Step 1: Register a Student

Run:

```bash
python catching_faces.py
```

Enter the student's name when prompted.

The webcam will open and begin collecting face samples. The program collects up to 100 samples and stores the resulting data in the `data` directory.

### Step 2: Run Face Recognition

Run:

```bash
python "testing of attendance.py"
```

The program loads the saved face data, trains the KNN classifier, and starts the webcam.

When a registered face is detected, the predicted name is displayed on the screen.

Press:

```text
O
```

to record the displayed student's attendance.

Press:

```text
Q
```

to exit the recognition program.

### Step 3: Open the Dashboard

Run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where the attendance dashboard can be accessed.

The dashboard displays the current day's attendance records and provides options for managing registered students.

## Data Storage

This project uses local files rather than a remote database.

### Student data

```text
data/names.pkl
data/faces_data.pkl
```

`names.pkl` stores the labels associated with the face samples, while `faces_data.pkl` stores the numerical face data.

### Attendance data

Attendance is stored as daily CSV files:

```text
Attendance/Attendance_DD-MM-YYYY.csv
```

Each attendance record contains:

```text
NAME,TIME
```

## Recognition Pipeline

The main recognition process can be summarized as:

```text
Student Registration
       ↓
Webcam Capture
       ↓
Haar Cascade Face Detection
       ↓
Face Cropping
       ↓
50 × 50 Image Resizing
       ↓
Numerical Feature Representation
       ↓
Local Dataset
       ↓
KNN Training
       ↓
Live Webcam Frame
       ↓
Face Detection
       ↓
Face Preprocessing
       ↓
KNN Prediction
       ↓
Student Name
       ↓
Date & Time
       ↓
CSV Attendance Record
```

## Design Approach

One of the main things I focused on while building the project was separating different responsibilities instead of putting everything into a single script.

* `catching_faces.py` handles data collection.
* `testing of attendance.py` handles recognition and attendance.
* `data_for_student.py` handles student data.
* `app.py` handles the dashboard.

This makes it easier to modify one part of the project without having to rewrite the entire application.

## Limitations

This project is intended as a learning and demonstration project rather than a production-grade biometric attendance system.

Some current limitations include:

* Recognition performance can depend on lighting and camera quality.
* The system relies on the Haar Cascade face detector.
* Face data is stored locally using Pickle files.
* The KNN model is trained when the recognition program starts.
* There is no database server or authentication system.
* The current implementation does not include advanced anti-spoofing or liveness detection.

## What I Learned

Through this project, I worked with several parts of a real computer-vision pipeline, including webcam input, face detection, image preprocessing, feature representation, machine-learning classification, file storage, and a web-based interface.

The project also helped me understand the importance of separating data collection, model processing, data management, and presentation into different parts of an application.

## Future Improvements

Some areas I would like to explore in future versions include:

* Using a more advanced face-recognition approach.
* Adding liveness detection.
* Moving from local files to a proper database.
* Improving recognition under different lighting conditions.
* Adding authentication for administrators.
* Improving the dashboard and attendance-management features.
* Adding better handling for multiple faces and duplicate attendance records.

## Author

**Aryan Patel**

This project was developed as a personal learning project to explore computer vision, machine learning, and Python application development.
