import os
import json
import pathspec
import sys

def read_project_repo(directory_path, language="python"):
    # Default patterns to ignore
    default_ignore_patterns = [
        '.git',
        '*.pyc',
        '__pycache__',
        '*.swp',
        '.DS_Store'
    ]

    # Try to read .gitignore or .gitignore.txt file
    gitignore_path = os.path.join(directory_path, ".gitignore")
    gitignore_txt_path = os.path.join(directory_path, ".gitignore.txt")

    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            gitignore_patterns = file.readlines()
        print(f"Using .gitignore file found at {gitignore_path}")
    elif os.path.exists(gitignore_txt_path):
        with open(gitignore_txt_path, 'r') as file:
            gitignore_patterns = file.readlines()
        print(f"Using .gitignore.txt file found at {gitignore_txt_path}")
    else:
        print("Warning: Neither .gitignore nor .gitignore.txt file found. Using default ignore patterns.")
        gitignore_patterns = []

    # Extend gitignore patterns with default patterns
    gitignore_patterns.extend(default_ignore_patterns)

    # Remove any empty lines and strip whitespace
    gitignore_patterns = [pattern.strip() for pattern in gitignore_patterns if pattern.strip()]

    spec = pathspec.PathSpec.from_lines('gitwildmatch', gitignore_patterns)

    # Initialize the repository structure
    repo_structure = {}

    # Traverse the project directory
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, directory_path)
            
            # Skip files and directories listed in .gitignore or default patterns
            if spec.match_file(relative_file_path):
                continue
            
            # Update the repository structure
            current_dir = repo_structure
            path_parts = relative_file_path.split(os.sep)[:-1]
            for part in path_parts:
                if part not in current_dir:
                    current_dir[part] = {}
                current_dir = current_dir[part]
            current_dir[file_name] = {'directory_path': file_path}

    return repo_structure

def print_directory_structure(structure, indent=0, last=False):
    result = []
    prefix = '└── ' if last else '├── '
    for i, (name, item) in enumerate(structure.items()):
        if isinstance(item, dict):
            if 'directory_path' in item:
                line = f"{' ' * indent}{prefix}{name}"
                print(line)
                result.append(line)
            else:
                line = f"{' ' * indent}{prefix}{name}/"
                print(line)
                result.append(line)
                substructure = print_directory_structure(item, indent + 4, i == len(structure) - 1)
                result.append(substructure)
    return "\n".join(result)

def directory(directory_path, language="python"):
    repo_structure = read_project_repo(directory_path, language)
    result = print_directory_structure(repo_structure)
    with open("./content/repo_structure.txt", "w", encoding='utf-8') as f:
        f.write(result)
    return repo_structure

if __name__ == "__main__":
    # The language flag is still used by the processing script,
    # but the directory function now builds a holistic file structure.
    language = "java" if "--java" in sys.argv else "python"
    if len(sys.argv) > 1:
        path_arg = sys.argv[1]
        print(f"Path received from command line: {path_arg}")
        directory(path_arg, language)
    else:
        print("No path provided.")
