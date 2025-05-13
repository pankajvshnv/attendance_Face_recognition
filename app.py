from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from face_detection_utils import (
    initialize_directories,
    load_face_encodings,
    load_students_data,
    update_attendance_excel
)

app = Flask(__name__)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/take_attendance', methods=['GET', 'POST'])
def take_attendance():
    """Handle the attendance taking process."""
    if request.method == 'POST':
        # Handle the taking attendance process here
        subject = request.form['subject']
        
        # Call the existing function to take attendance here
        # For example: take_attendance_function(subject)

        # You can use the webcam or integrate it as a service
        return render_template('attendance.html', subject=subject)
    
    # Show available subjects
    students_data = load_students_data()
    all_subjects = set()
    for data in students_data.values():
        all_subjects.update(data.get("subjects", []))
    
    subjects_list = sorted(list(all_subjects))
    return render_template('attendance.html', subjects=subjects_list)

@app.route('/mark_absentees', methods=['GET', 'POST'])
def mark_absentees():
    """Mark students as absent."""
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        
        # Call the function to mark absentees
        # For example: mark_absentees_function(subject, date)
        
        return redirect(url_for('index'))

    students_data = load_students_data()
    all_subjects = set()
    for data in students_data.values():
        all_subjects.update(data.get("subjects", []))
    
    subjects_list = sorted(list(all_subjects))
    return render_template('absentees.html', subjects=subjects_list)

if __name__ == '__main__':
    app.run(debug=True)
