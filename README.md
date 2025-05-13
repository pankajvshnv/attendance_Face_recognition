# Face Recognition Attendance System

A complete Python-based attendance system using face recognition technology that can register students, mark attendance via webcam, and generate detailed reports.

## Features

- **Face Registration**: Add new students with their face data and details
- **Face Recognition**: Automatically mark attendance when a registered face is detected
- **Attendance Tracking**: Store and manage attendance records in Excel
- **Reporting**: Generate detailed attendance reports with percentages and visualizations

## Project Structure

```
face_attendance_project/
├── main.py                  # Main program entry point
├── face_detection_utils.py  # Utility functions for face detection
├── register_faces.py        # For registering new student faces
├── take_attendance.py       # For taking attendance with webcam
├── calculate_report.py      # For generating attendance reports
├── requirements.txt         # Python dependencies
├── faces/                   # Directory to store face images and data
│   ├── encodings.pkl        # Face encodings data
│   └── students.pkl         # Student information data
├── attendance.xlsx          # Excel file storing attendance records
└── attendance_charts/       # Directory for attendance visualizations
```

## Requirements

- Python 3.6 or higher
- Webcam for face detection
- Required Python packages (see requirements.txt)

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

**Note for Windows users**: You might need to install Visual C++ build tools first for the face_recognition library. See [face_recognition installation guide](https://github.com/ageitgey/face_recognition#installation-options) for details.

## Usage

### Running the program

Run the main program:

```bash
python main.py
```

This will present you with the main menu:

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                FACE RECOGNITION ATTENDANCE SYSTEM                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

===== MAIN MENU =====
1. Register Students
2. Take Attendance
3. Generate Attendance Reports
4. Exit
```

### Registering Students

1. Select option 1
2. Enter student details (name, roll number, semester, year)
3. Enter the subjects for the student
4. Position your face in front of the webcam and press 'c' to capture

### Taking Attendance

1. Select option 2
2. Choose between taking attendance or marking absentees
3. Select the subject for which to mark attendance
4. When taking attendance, the system will automatically recognize faces from the webcam
5. Press 'q' to stop attendance marking

### Generating Reports

1. Select option 3
2. The system will generate a comprehensive Excel report with multiple sheets:
   - Overall Report
   - Subject-wise Report
   - Student-wise Report
   - Daily Attendance Report
3. Visual charts will also be generated in the attendance_charts directory

## Key Files

- **main.py**: Entry point that connects all components
- **face_detection_utils.py**: Core functions for face detection and recognition
- **register_faces.py**: Handles student registration
- **take_attendance.py**: Manages face detection and attendance marking
- **calculate_report.py**: Generates Excel reports and visualizations

## Troubleshooting

- **Face recognition issues**: Make sure your face is well-lit when registering and taking attendance
- **DLL load failed error on Windows**: Install Visual C++ build tools
- **Camera not found**: Make sure your webcam is properly connected and not being used by another application

## Customization

- Adjust the minimum attendance percentage in `calculate_report.py` by changing the `MIN_ATTENDANCE_PERCENTAGE` constant
- Modify the face recognition tolerance in `face_detection_utils.py` in the `recognize_faces` function