import os
import shutil
import time


SAMPLE_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'file_processor', 'data', 'uploads')

def copy_sample_files():
    """Copy sample files to the upload directory for testing"""
    print("=" * 60)
    print("File Processing Pipeline - Test Script")
    print("=" * 60)

    if not os.path.exists(SAMPLE_FILES_DIR):
        print(f"Error: Sample files directory not found: {SAMPLE_FILES_DIR}")
        return

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    print(f"\nCopying sample files to: {UPLOAD_DIR}\n")

    for filename in os.listdir(SAMPLE_FILES_DIR):
        src = os.path.join(SAMPLE_FILES_DIR, filename)
        dst = os.path.join(UPLOAD_DIR, filename)

        if os.path.isfile(src):
            print(f"Copying: {filename}")
            shutil.copy2(src, dst)
            time.sleep(2)  # Wait 2 seconds between files

    print("\n" + "=" * 60)
    print("All sample files copied!")
    print("Check the web UI at http://localhost:5000 to see the events")
    print("=" * 60)

if __name__ == '__main__':
    print("\nMake sure the application is running (python file_processor/app.py)")
    input("Press Enter to copy sample files to the upload directory...")
    copy_sample_files()
