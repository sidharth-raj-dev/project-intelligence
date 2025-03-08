import os
import glob
from directory import directory
import sys
import io
import subprocess

def process(directory_structure, flag=None, language="python"):
    # Iterate over each item in the directory structure
    for key, value in directory_structure.items():
        if 'directory_path' in value:  # It's a file
            file_path = value['directory_path']
            # Check file extension and call the proper skeleton script.
            if file_path.endswith('.java'):
                # If we're processing Java files, call skeleton_java.py
                if language != "java":
                    continue  # Skip if the language flag is not set to java
                print(f"{file_path}............................................")
                if flag == '--verbose':
                    command = ["python", "skeleton_java.py", file_path, "--verbose", "--java"]
                elif flag == '--import':
                    command = ["python", "skeleton_java.py", file_path, "--import", "--java"]
                else:
                    command = ["python", "skeleton_java.py", file_path, "--java"]
            elif file_path.endswith('.py'):
                # Process Python files with skeleton.py if language flag is set to python.
                if language != "python":
                    continue  # Skip if the language flag is not set to python
                print(f"{file_path}............................................")
                if flag == '--verbose':
                    command = ["python", "skeleton.py", file_path, "--verbose"]
                elif flag == '--import':
                    command = ["python", "skeleton.py", file_path, "--import"]
                else:
                    command = ["python", "skeleton.py", file_path]
            else:
                continue  # Skip files that are not .py or .java
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
        else:
            process(value, flag, language)  # Recursively process sub-directories

def capture_console_output(func, *args, **kwargs):
    buffer = io.StringIO()
    stdout = sys.stdout
    sys.stdout = buffer
    func(*args, **kwargs)
    sys.stdout = stdout
    console_output = buffer.getvalue()
    buffer.close()
    return console_output

if __name__ == "__main__":
    # Set language based on flag; this controls which files get processed.
    language = "java" if "--java" in sys.argv else "python"
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
        print(f"path received from command line: {root_path}")
        input_structure = directory(root_path, language)
        
        mode = None
        if '--verbose' in sys.argv:
            mode = '--verbose'
        elif '--import' in sys.argv:
            mode = '--import'
        
        console_output = capture_console_output(process, input_structure, mode, language)
        print(console_output)

        with open('content/processed.txt', 'w') as file:
            file.write(console_output)
    else:
        print("no path provided.")
