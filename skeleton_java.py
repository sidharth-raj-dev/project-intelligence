import sys
import re

def find_imports(code):
    # Match Java import statements (e.g., import java.util.List;)
    imports = re.findall(r'^\s*import\s+([\w\.]+);', code, re.MULTILINE)
    for imp in imports:
        print(f"import {imp}")

def find_annotations(code):
    """
    Find Java annotations of the form:
        @Annotation
        @Annotation(params)
    and print them.
    """
    # This pattern captures:
    #   1. The annotation name (e.g. Override, RequestMapping)
    #   2. Any optional parameters in parentheses (e.g. (\"/hello\")), which may be empty
    annotation_pattern = re.compile(r'@\s*([\w.]+)(\([^)]*\))?', re.MULTILINE)
    annotations = annotation_pattern.findall(code)
    for ann in annotations:
        # ann is a tuple (annotationName, annotationParams)
        annotation_name = ann[0]
        annotation_params = ann[1]
        # Print them together, e.g. "Annotation: Override" or "Annotation: RequestMapping(\"/hello\")"
        print(f"Annotation: {annotation_name}{annotation_params}")

def generate_dependency_graph(code):
    # Extract method definitions and method calls in a simplistic way
    method_def_pattern = re.compile(
        r'\s*(public|private|protected)?\s*(static\s+)?[\w<>\[\]]+\s+(\w+)\s*\((.*?)\)\s*\{'
    )
    methods = method_def_pattern.findall(code)
    function_calls = {}
    for m in methods:
        method_name = m[2]
        function_calls[method_name] = []
        # Find method calls using a simple regex
        call_pattern = re.compile(r'(\w+)\s*\(')
        calls = call_pattern.findall(code)
        # Filter out the method name itself and remove duplicates
        calls = [call for call in calls if call != method_name]
        function_calls[method_name] = list(set(calls))
    for method, calls in function_calls.items():
        print(method)
        for call in calls:
            print(f'    {call}')

def verbose_analysis(code):
    # Print package declaration if present
    package_pattern = re.compile(r'^\s*package\s+([\w\.]+);', re.MULTILINE)
    package_match = package_pattern.search(code)
    if package_match:
        print("Package:", package_match.group(1))

    # Print class declarations
    class_pattern = re.compile(r'\s*public\s+class\s+(\w+)\s*\{')
    classes = class_pattern.findall(code)
    for cls in classes:
        print("Class:", cls)

    # Print annotations
    find_annotations(code)

    # Print imports
    find_imports(code)

    # Print dependency graph
    generate_dependency_graph(code)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        if '--import' in sys.argv:
            find_imports(code)
            generate_dependency_graph(code)
        elif '--verbose' in sys.argv:
            verbose_analysis(code)
        else:
            generate_dependency_graph(code)
    else:
        print("no file path provided.")
