"""
Script to calculate attendance reports and percentages.
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from face_detection_utils import initialize_directories, load_students_data

# Constant for the minimum required attendance percentage
MIN_ATTENDANCE_PERCENTAGE = 75

def generate_attendance_report(output_file=None):
    """
    Generate attendance report with percentages for all students.
    
    Args:
        output_file: Path to save the output Excel report (optional)
    """
    # Initialize directories
    initialize_directories()
    
    # Load student data
    students_data = load_students_data()
    
    if not students_data:
        print("No students registered yet. Please register students first.")
        return
    
    # Check if attendance file exists
    attendance_file = "attendance.xlsx"
    if not os.path.exists(attendance_file):
        print("No attendance records found. Please take attendance first.")
        return
    
    try:
        # Load attendance data
        df = pd.read_excel(attendance_file)
        
        if df.empty:
            print("No attendance records found in the file.")
            return
        
        # Default output file if not specified
        if output_file is None:
            current_date = datetime.now().strftime("%Y%m%d")
            output_file = f"attendance_report_{current_date}.xlsx"
        
        # Create Excel writer
        with pd.ExcelWriter(output_file) as writer:
            # 1. Overall Report Sheet
            create_overall_report(df, students_data, writer)
            
            # 2. Subject-wise Report Sheet
            create_subject_wise_report(df, students_data, writer)
            
            # 3. Student-wise Report Sheet
            create_student_wise_report(df, students_data, writer)
            
            # 4. Daily Attendance Sheet
            create_daily_attendance_report(df, writer)
        
        print(f"\nAttendance report generated successfully: {output_file}")
        
        # Visualize attendance data
        visualize_attendance_data(df, students_data)
        
    except Exception as e:
        print(f"Error generating report: {e}")

def create_overall_report(df, students_data, writer):
    """Create overall attendance report sheet."""
    print("\nGenerating overall attendance report...")
    
    # Get all subjects
    all_subjects = set()
    for data in students_data.values():
        all_subjects.update(data.get("subjects", []))
    
    # Create a list to store results
    results = []
    
    # Calculate for each student
    for roll_no, data in students_data.items():
        student_name = data["name"]
        student_subjects = data.get("subjects", [])
        
        # Filter attendance records for this student
        student_df = df[df["Roll No"] == roll_no]
        
        # Create a dictionary for this student
        student_result = {
            "Roll No": roll_no,
            "Name": student_name,
            "Semester": data.get("semester", "N/A"),
            "Year": data.get("year", "N/A")
        }
        
        # Total classes (counting both present and absent)
        total_classes = len(student_df)
        attended_classes = len(student_df[student_df["Status"] == "Present"])
        
        if total_classes > 0:
            overall_percentage = (attended_classes / total_classes) * 100
        else:
            overall_percentage = 0
        
        student_result["Total Classes"] = total_classes
        student_result["Attended Classes"] = attended_classes
        student_result["Overall Percentage"] = round(overall_percentage, 2)
        student_result["Status"] = "Good" if overall_percentage >= MIN_ATTENDANCE_PERCENTAGE else "Low"
        
        # Add to results
        results.append(student_result)
    
    # Create DataFrame
    overall_df = pd.DataFrame(results)
    
    # Sort by roll number
    overall_df = overall_df.sort_values("Roll No")
    
    # Apply conditional formatting to highlight low attendance
    def highlight_low_attendance(val):
        if isinstance(val, (int, float)) and isinstance(val, str) is False:
            if val < MIN_ATTENDANCE_PERCENTAGE:
                return 'background-color: #FF9999'  # Light red color
        if val == "Low":
            return 'background-color: #FF9999'  # Light red color
        return ''
    
    # Convert to Excel
    overall_df.style.applymap(highlight_low_attendance).to_excel(writer, sheet_name="Overall Report", index=False)
    
    # Adjust column widths
    worksheet = writer.sheets["Overall Report"]
    for i, col in enumerate(overall_df.columns):
        max_length = max(overall_df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, max_length)

def create_subject_wise_report(df, students_data, writer):
    """Create subject-wise attendance report sheet."""