"""
Script to detect faces and mark attendance.
"""
import cv2
import face_recognition
import numpy as np
import tzl_nos]
    
    # Select subject for marking attendance
    print("\nAvailable subjects:")
    all_subjects = set()
    for data in students_data.values():
        all_subjects.update(data.get("subjects", []))
    
    # Create numbered list of subjects
    subjects_list = sorted(list(all_subjects))
    for i, subject in enumerate(subjects_list, 1):
        print(f"{i}. {subject}")
    
    # Get subject selection
    while True:
        try:
            subject_index = int(input("\nSelect subject number for attendance: ")) - 1
            if 0 <= subject_index < len(subjects_list):
                selected_subject = subjects_list[subject_index]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\nTaking attendance for subject: {selected_subject}")
    print("Press 'q' to stop attendance.")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Set to store students already marked present
    marked_students = set()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Resize frame for faster processing (optional)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Detect faces
        face_locations, face_encodings = detect_faces(small_frame)
        
        # Scale back face locations
        face_locations = [(top * 4, right * 4, bottom * 4, left * 4) 
                         for top, right, bottom, left in face_locations]
        
        # Recognize faces
        face_names = recognize_faces(face_encodings, known_face_encodings, names)
        
        # Draw boxes around faces
        frame = draw_face_boxes(frame, face_locations, face_names)
        
        # Mark attendance for recognized students
        for name in face_names:
            if name != "Unknown" and name not in marked_students:
                # Find the roll number for this student
                student_roll_no = None
                for roll_no, data in students_data.items():
                    if data["name"] == name:
                        student_roll_no = roll_no
                        
                        # Check if student is enrolled in this subject
                        if selected_subject not in data.get("subjects", []):
                            print(f"{name} is not enrolled in {selected_subject}")
                            continue
                        
                        break
                
                if student_roll_no:
                    success = update_attendance_excel(name, student_roll_no, selected_subject)
                    if success:
                        marked_students.add(name)
                        
                        # Display confirmation message on screen
                        cv2.putText(frame, f"Attendance marked for {name}!", 
                                  (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Show the frame with the message for 2 seconds
                        cv2.imshow("Attendance System", frame)
                        cv2.waitKey(2000)
        
        # Add info text
        cv2.putText(frame, f"Subject: {selected_subject}", 
                  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Show number of students marked
        cv2.putText(frame, f"Marked: {len(marked_students)}", 
                  (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow("Attendance System", frame)
        
        # Break loop on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release webcam and close windows
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\nAttendance completed for {selected_subject}.")
    print(f"Total students marked present: {len(marked_students)}")
    print("Attendance has been saved to attendance.xlsx")

def mark_absentees():
    """Mark absent students for a subject on a specific date."""
    # Initialize required directories
    initialize_directories()
    
    # Load student data
    students_data = load_students_data()
    
    if not students_data:
        print("No students registered yet. Please register students first.")
        return
    
    # Select subject for marking attendance
    print("\nAvailable subjects:")
    all_subjects = set()
    for data in students_data.values():
        all_subjects.update(data.get("subjects", []))
    
    subjects_list = sorted(list(all_subjects))
    for i, subject in enumerate(subjects_list, 1):
        print(f"{i}. {subject}")
    
    # Get subject selection
    while True:
        try:
            subject_index = int(input("\nSelect subject number for marking absentees: ")) - 1
            if 0 <= subject_index < len(subjects_list):
                selected_subject = subjects_list[subject_index]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get date (default to today)
    date_input = input("\nEnter date for attendance (YYYY-MM-DD) or press Enter for today: ")
    if date_input.strip():
        try:
            attendance_date = datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using today's date.")
            attendance_date = datetime.now().strftime("%Y-%m-%d")
    else:
        attendance_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get list of students enrolled in this subject
    enrolled_students = []
    for roll_no, data in students_data.items():
        if selected_subject in data.get("subjects", []):
            enrolled_students.append((data["name"], roll_no))
    
    # Check which students are already marked present
    import pandas as pd
    
    attendance_file = "attendance.xlsx"
    
    if not os.path.exists(attendance_file):
        present_students = []
    else:
        try:
            df = pd.read_excel(attendance_file)
            present_students = df[(df["Date"] == attendance_date) & 
                                (df["Subject"] == selected_subject) &
                                (df["Status"] == "Present")]["Name"].tolist()
        except Exception as e:
            print(f"Error reading attendance file: {e}")
            present_students = []
    
    # Find absent students
    absent_students = [(name, roll_no) for name, roll_no in enrolled_students if name not in present_students]
    
    if not absent_students:
        print(f"All students are already marked present for {selected_subject} on {attendance_date}.")
        return
    
    # Mark absent students
    print(f"\nMarking absent students for {selected_subject} on {attendance_date}:")
    for i, (name, roll_no) in enumerate(absent_students, 1):
        print(f"{i}. {name} (Roll No: {roll_no})")
    
    confirm = input("\nMark all these students as absent? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Mark students as absent
    for name, roll_no in absent_students:
        update_attendance_excel(name, roll_no, selected_subject, status="Absent", file_path=attendance_file)
    
    print(f"\nSuccessfully marked {len(absent_students)} students as absent for {selected_subject} on {attendance_date}.")
    print("Attendance has been updated in attendance.xlsx")

def main():
    """Main function to run the attendance system."""
    while True:
        print("\n===== Attendance System =====")
        print("1. Take Attendance")
        print("2. Mark Absentees")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            take_attendance()
        elif choice == '2':
            mark_absentees()
        elif choice == '3':
            print("Exiting attendance system...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
