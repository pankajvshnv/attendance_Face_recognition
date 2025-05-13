"""
Utility functions for face detection and recognition.
"""
import os
import cv2
import face_recognition
import numpy as np
import pickle
from datetime import datetime
import pandas as pd

# Constants
FACES_DIR = 'faces'
ENCODINGS_FILE = os.path.join(FACES_DIR, 'encodings.pkl')
STUDENTS_FILE = os.path.join(FACES_DIR, 'students.pkl')

def initialize_directories():
    """Create necessary directories if they don't exist."""
    if not os.path.exists(FACES_DIR):
        os.makedirs(FACES_DIR)
    
    # Initialize empty encodings and students data if they don't exist
    if not os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, 'wb') as f:
            pickle.dump([], f)
    
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'wb') as f:
            pickle.dump({}, f)

def load_face_encodings():
    """Load saved face encodings."""
    try:
        with open(ENCODINGS_FILE, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def load_students_data():
    """Load saved student information."""
    try:
        with open(STUDENTS_FILE, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {}

def save_face_encodings(encodings):
    """Save face encodings to disk."""
    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump(encodings, f)

def save_students_data(students_data):
    """Save student information to disk."""
    with open(STUDENTS_FILE, 'wb') as f:
        pickle.dump(students_data, f)

def detect_faces(frame):
    """
    Detect faces in the given frame.
    
    Args:
        frame: The image frame to detect faces in
        
    Returns:
        face_locations: List of face locations in (top, right, bottom, left) format
        face_encodings: List of 128-dimensional face encodings
    """
    # Convert BGR to RGB (face_recognition uses RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    return face_locations, face_encodings

def recognize_faces(face_encodings, known_face_encodings, known_face_names):
    """
    Recognize faces by comparing them to known face encodings.
    
    Args:
        face_encodings: List of face encodings to recognize
        known_face_encodings: List of known face encodings
        known_face_names: List of names corresponding to known_face_encodings
        
    Returns:
        List of names for the recognized faces
    """
    face_names = []
    
    for face_encoding in face_encodings:
        # Compare faces with the known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"
        
        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        
        face_names.append(name)
    
    return face_names

def draw_face_boxes(frame, face_locations, face_names):
    """
    Draw boxes and labels around detected faces.
    
    Args:
        frame: The image frame to draw on
        face_locations: List of face locations in (top, right, bottom, left) format
        face_names: List of names corresponding to the face_locations
        
    Returns:
        The frame with boxes and labels drawn
    """
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
    
    return frame

def update_attendance_excel(student_name, roll_no, subject, status="Present", file_path="attendance.xlsx"):
    """
    Update attendance in Excel sheet.
    
    Args:
        student_name: Name of the student
        roll_no: Roll number of the student
        subject: Subject name
        status: Attendance status (Present/Absent)
        file_path: Path to Excel file
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Create a new DataFrame if file doesn't exist
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Name", "Roll No", "Date", "Time", "Subject", "Status"])
    else:
        try:
            df = pd.read_excel(file_path)
        except Exception:
            df = pd.DataFrame(columns=["Name", "Roll No", "Date", "Time", "Subject", "Status"])
    
    # Check if student already marked attendance for this subject today
    today_records = df[(df["Date"] == current_date) & 
                       (df["Name"] == student_name) & 
                       (df["Subject"] == subject)]
    
    if not today_records.empty:
        print(f"{student_name} already marked attendance for {subject} today!")
        return False
    
    # Add new attendance record
    new_record = {
        "Name": student_name,
        "Roll No": roll_no,
        "Date": current_date,
        "Time": current_time,
        "Subject": subject,
        "Status": status
    }
    
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    
    # Save to Excel
    df.to_excel(file_path, index=False)
    print(f"Attendance marked for {student_name} in {subject}")
    return True