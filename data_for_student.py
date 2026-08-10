import pickle
from pathlib import Path
import numpy as np

# File and directory paths
DATA_DIR = Path(__file__).resolve().parent / "data"
NAMES_FILE = DATA_DIR / "names.pkl"
FACES_FILE = DATA_DIR / "faces_data.pkl"


def _ensure_data_dir():
    # Helper function to create the 'data' directory if it doesn't exist yet
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_student_names():
    # Loads and returns the list of student names from names.pkl
    if not NAMES_FILE.exists():
        return []

    with open(NAMES_FILE, "rb") as handle:
        data = pickle.load(handle)

    return list(data)


def load_student_faces():
    # Loads and returns face matrix data from faces_data.pkl
    if not FACES_FILE.exists():
        return np.empty((0, 0), dtype=np.float32)

    with open(FACES_FILE, "rb") as handle:
        data = pickle.load(handle)

    # Convert to numpy array if it isn't one already
    if isinstance(data, np.ndarray):
        return data

    return np.asarray(data, dtype=np.float32)


def list_students():
    # Returns an alphabetized list of unique student names
    return sorted(set(load_student_names()))


def save_student_faces(name, face_batch):
    # Saves face data along with the student's name
    _ensure_data_dir()

    # Make sure face data is a 2D numpy array
    batch = np.asarray(face_batch)
    if batch.ndim == 1:
        batch = batch.reshape(1, -1)

    # Update and save the student names list
    names = load_student_names()
    names.extend([name] * len(batch))

    with open(NAMES_FILE, "wb") as handle:
        pickle.dump(names, handle)

    # Combine existing face data with the new face batch and save
    existing_faces = load_student_faces()
    if existing_faces.size == 0:
        combined_faces = batch
    else:
        combined_faces = np.vstack([existing_faces, batch])

    with open(FACES_FILE, "wb") as handle:
        pickle.dump(combined_faces, handle)

    return len(batch)


def delete_student(name):
    # Removes all data associated with a student name
    names = load_student_names()

    # If list is empty or student isn't found, return False
    if not names or name not in names:
        return False

    # Create a boolean list: True to keep, False for the student being deleted
    keep_mask = [student_name != name for student_name in names]
    remaining_names = [
        student_name
        for student_name, keep in zip(names, keep_mask)
        if keep
    ]

    # Filter out face data corresponding to the deleted student
    faces = load_student_faces()
    if faces.size == 0:
        remaining_faces = faces
    else:
        remaining_faces = faces[np.array(keep_mask)]

    # Save updated data back to files
    _ensure_data_dir()

    with open(NAMES_FILE, "wb") as handle:
        pickle.dump(remaining_names, handle)

    with open(FACES_FILE, "wb") as handle:
        pickle.dump(remaining_faces, handle)

    return True
