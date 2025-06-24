"""
Script to register new students with their face encodings.
"""
import os
import cv2
import face_recognition
import pickle
import time
import numpy as np
from face_detection_utils import (
    FACES_DIR, 
    initialize_directories, 
    load_face_encodings, 
    load_students_data, 
    save_face_encodings, 
    save_students_data
)

def register_new_student():
    """Register a new student with their face and information."""
    # Initialize required directories
    initialize_directories()
    
    # Load existing data
    known_face_encodings = load_face_encodings()
    students_data = load_students_data()
    
    # Get student details
    name = input("Enter student name: ")
    roll_no = input("Enter roll number: ")
    
    # Check if student already exists
    if roll_no in students_data:
        print(f"Student with roll number {roll_no} already exists!")
        overwrite = input("Do you want to overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            return
    
    semester = input("Enter semester (e.g., 1, 2, 3): ")
    year = input("Enter year (e.g., 2023): ")
    
    # Get subject list
    subjects = []
    num_subjects = int(input("Enter number of subjects: "))
    for i in range(num_subjects):
        subject = input(f"Enter subject {i+1}: ")
        subjects.append(subject)
    
    # Capture face image using webcam
    print("\nPreparing to capture face...")
    print("Position your face in front of the camera.")
    print("Press 'c' to capture, 'r' to retake, or 'q' to quit.")
    
    cap = cv2.VideoCapture(0)
    face_encoding = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Display the frame
        display_frame = frame.copy()
        cv2.putText(display_frame, "Press 'c' to capture, 'r' to retake, 'q' to quit", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Detect faces in the frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        
        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(display_frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        cv2.imshow("Register Face", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Registration cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            return
        
        elif key == ord('c'):
            if len(face_locations) == 0:
                print("No face detected! Please position yourself properly.")
                continue
            
            if len(face_locations) > 1:
                print("Multiple faces detected! Please ensure only one face is visible.")
                continue
            
            # Get the face encoding
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            
            # Show the captured image
            cv2.putText(display_frame, "Face captured! Press 'r' to retake or any other key to continue.", 
                      (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Register Face", display_frame)
            
            key = cv2.waitKey(0) & 0xFF
            if key == ord('r'):
                print("Retaking capture...")
                continue
            else:
                break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if face_encoding is None:
        print("No face was captured. Registration failed.")
        return
    
    # Save the face image
    student_image_path = os.path.join(FACES_DIR, f"{roll_no}.jpg")
    cv2.imwrite(student_image_path, frame)
    
    # Update encodings and student data
    known_face_encodings.append(face_encoding)
    
    students_data[roll_no] = {
        "name": name,
        "roll_no": roll_no,
        "semester": semester,
        "year": year,
        "subjects": subjects,
        "image_path": student_image_path
    }
    
    # Save updated data
    save_face_encodings(known_face_encodings)
    save_students_data(students_data)
    
    print(f"\nStudent {name} (Roll No: {roll_no}) registered successfully!")

def view_registered_students():
    """View all registered students."""
    students_data = load_students_data()
    
    if not students_data:
        print("No students registered yet!")
        return
    
    print("\n===== Registered Students =====")
    print(f"{'Name':<20} {'Roll No':<10} {'Semester':<10} {'Year':<6} {'Subjects'}")
    print("="*70)
    
    for roll_no, data in students_data.items():
        subjects_str = ", ".join(data.get("subjects", []))
        print(f"{data['name']:<20} {roll_no:<10} {data['semester']:<10} {data['year']:<6} {subjects_str}")
    
    print("="*70)

def delete_student():
    """Delete a registered student."""
    students_data = load_students_data()
    known_face_encodings = load_face_encodings()
    
    if not students_data:
        print("No students registered yet!")
        return
    
    roll_no = input("Enter roll number of student to delete: ")
    
    if roll_no not in students_data:
        print(f"No student found with roll number {roll_no}!")
        return
    
    student = students_data[roll_no]
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete {student['name']} (Roll No: {roll_no})? (y/n): ")
    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return
    
    # Remove student data
    student_index = list(students_data.keys()).index(roll_no)
    del students_data[roll_no]
    
    # Remove face encoding
    if student_index < len(known_face_encodings):
        known_face_encodings.pop(student_index)
    
    # Remove face image if exists
    image_path = student.get("image_path")
    if image_path and os.path.exists(image_path):
        os.remove(image_path)
    
    # Save updated data
    save_face_encodings(known_face_encodings)
    save_students_data(students_data)
    
    print(f"Student {student['name']} (Roll No: {roll_no}) deleted successfully!")

def main():
    """Main function to run the registration system."""
    initialize_directories()
    
    while True:
        print("\n===== Face Registration System =====")
        print("1. Register New Student")
        print("2. View Registered Students")
        print("3. Delete Student")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            register_new_student()
        elif choice == '2':
            view_registered_students()
        elif choice == '3':
            delete_student()
        elif choice == '4':
            print("Exiting registration system...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
