"""
Main script to run the Face Recognition Attendance System.
"""
import os
import sys
import time
from face_detection_utils import initialize_directories

def print_banner():
    """Print welcome banner for the application."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║                FACE RECOGNITION ATTENDANCE SYSTEM                    ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def create_project_structure():
    """Create project folder structure if it doesn't exist."""
    # Create faces directory
    if not os.path.exists('faces'):
        os.makedirs('faces')
        print("Created 'faces' directory.")
    
    # Create attendance_charts directory
    if not os.path.exists('attendance_charts'):
        os.makedirs('attendance_charts')
        print("Created 'attendance_charts' directory.")
    
    # Initialize other required directories
    initialize_directories()
    print("Project structure initialized successfully.")

def main_menu():
    """Display main menu and handle user choices."""
    while True:
        print_banner()
        print("\n===== MAIN MENU =====")
        print("1. Register Students")
        print("2. Take Attendance")
        print("3. Generate Attendance Reports")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            # Import and run registration system
            from register_faces import main as register_main
            register_main()
        elif choice == '2':
            # Import and run attendance system
            from take_attendence import main as attendance_main
            attendance_main()
        elif choice == '3':
            # Import and run report system
            from calculate_report import main as report_main
            report_main()
        elif choice == '4':
            print("\nThank you for using Face Recognition Attendance System.")
            print("Exiting...\n")
            time.sleep(1)
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    # Setup project structure
    create_project_structure()
    
    # Run main menu
    main_menu()
