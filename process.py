import os
import glob
from skeleton import find_imports
from skeleton import generate_dependency_graph
from directory import directory
import sys
import json
import io
import subprocess

def process(directory_structure, flag=None):
    # Iterate over each item in the directory structure
    for key, value in directory_structure.items():
        if 'directory_path' in value:  # It's a file
            if key.endswith('.py'):  # Check if it's a .py file
                print(f"{value['directory_path']}............................................")
                with open(value['directory_path'], 'r', encoding='utf-8') as file:
                    code = file.read()

                if flag == '--verbose':
                    # Run the selected functions on the file content
                    command = ["python", "skeleton.py", f"{value['directory_path']}", "--verbose"]
                    result = subprocess.run(command, capture_output=True, text=True)
                    print(result.stdout)
                elif flag == '--import':
                    # Run the selected functions on the file content
                    command = ["python", "skeleton.py", f"{value['directory_path']}", "--import"]
                    result = subprocess.run(command, capture_output=True, text=True)
                    print(result.stdout)
                else:
                    command = ["python", "skeleton.py", f"{value['directory_path']}"]
                    result = subprocess.run(command, capture_output=True, text=True)
                    print(result.stdout)

        else:  # It's a directory
            process(value, flag)  # Recursively process the sub-directory

def capture_console_output(func, *args, **kwargs):
    # Create a string buffer
    buffer = io.StringIO()

    # Save the current stdout
    stdout = sys.stdout

    # Redirect stdout to the buffer
    sys.stdout = buffer

    # Execute the function
    func(*args, **kwargs)

    # Restore the original stdout
    sys.stdout = stdout

    # Get the console output from the buffer
    console_output = buffer.getvalue()

    # Close the buffer
    buffer.close()

    return console_output

if __name__ == "__main__":
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
        print(f"path received from command line: {root_path}")
        input_structure = directory(root_path)
        
        if '--verbose' in sys.argv:
            console_output = capture_console_output(process, input_structure, '--verbose')
            print(console_output)

        elif '--import' in sys.argv:
            console_output = capture_console_output(process, input_structure, '--import')
            print(console_output)
        else:
            console_output = capture_console_output(process, input_structure)
            print(console_output)

        with open('content/processed.txt', 'w') as file:
            file.write(console_output)
    else:
        print("no path provided.")

# Example usage
# root_path = 'C:/Users/sidha/projects/project-intelligence'
# input_structure = directory(root_path)
# process(input_structure, root_path)

# commands: python .\process.py C:\Users\sidha\projects\project-intelligence --verbose