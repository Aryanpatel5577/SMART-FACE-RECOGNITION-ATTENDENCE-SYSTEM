import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

# Custom functions imported from our database helper module
from data_for_student import delete_student, list_students

# Set the dashboard main heading
st.title("Attendance Dashboard")

# Get current date and time values
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

# Try importing the auto-refresh component if installed
try:
    from streamlit_autorefresh import st_autorefresh
except ImportError:
    st_autorefresh = None

# Automatically refresh the page every 2 seconds if the package is available
if st_autorefresh is not None:
    count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")
else:
    count = 0

# Display FizzBuzz logic output on screen based on refresh count
if count == 0:
    st.write("Count is zero")
elif count % 3 == 0 and count % 5 == 0:
    st.write("FizzBuzz")
elif count % 3 == 0:
    st.write("Fizz")
elif count % 5 == 0:
    st.write("Buzz")
else:
    st.write(f"Count: {count}")

# Student Management Section
st.subheader("Manage students")

# Fetch current registered students
student_options = list_students()

if student_options:
    # Dropdown menu to select a student
    selected_student = st.selectbox("Select a student to remove", student_options)

    # Button to confirm deletion
    if st.button("Delete selected student"):
        removed = delete_student(selected_student)
        if removed:
            st.success(f"Removed {selected_student}")
            st.rerun()
        else:
            st.error("Could not remove the selected student")
else:
    st.info("No students registered yet.")

# Attendance Display Section
attendance_path = Path("Attendance") / f"Attendance_{date}.csv"

# Load and show today's attendance records if the file exists
if attendance_path.exists():
    df = pd.read_csv(attendance_path)
    if df.empty:
        st.info("No attendance records yet for today.")
    else:
        st.dataframe(df.style.highlight_max(axis=0))
else:
    st.info("No attendance file found for today yet.")
    st.dataframe(pd.DataFrame(columns=["NAME", "TIME"]))