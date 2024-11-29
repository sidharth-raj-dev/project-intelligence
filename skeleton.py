import ast
import sys
import re

def generate_dependency_graph(code):
    class FunctionVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None
            self.function_calls = {}

        def visit_FunctionDef(self, node):
            self.current_function = node.name
            self.function_calls[self.current_function] = []
            self.generic_visit(node)
            self.current_function = None

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                if self.current_function:
                    self.function_calls[self.current_function].append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                if self.current_function:
                    # This will append the method call in the format `class.method`
                    self.function_calls[self.current_function].append(node.func.attr)
            self.generic_visit(node)

    tree = ast.parse(code)
    visitor = FunctionVisitor()
    visitor.visit(tree)

    for function, calls in visitor.function_calls.items():
        print(function)
        for call in calls:
            print(f'    {call}')

def find_imports(code):
    class ImportVisitor(ast.NodeVisitor):
        def visit_Import(self, node):
            for alias in node.names:
                print(f"import {alias.name}")

        def visit_ImportFrom(self, node):
            for alias in node.names:
                print(f"from {node.module} import {alias.name}")

    tree = ast.parse(code)
    visitor = ImportVisitor()
    visitor.visit(tree)

class CodeParser:
    def __init__(self):
        self.class_pattern = re.compile(r'^.*class (\w+):')
        self.method_pattern = re.compile(r'^.*def (\w+)\((.*?)\):')
        self.call_pattern = re.compile(r'\s*(\w+)\((.*?)\)')
        self.return_pattern = re.compile(r'^.*return (.*)')
        self.current_class = None
        self.current_method = None
        self.methods = {}

    def parse_line(self, line):
        class_match = self.class_pattern.search(line)
        if class_match:
            class_name = class_match.group(1)
            self.current_class = class_name
            self.methods[self.current_class] = {}
            print(f'class {class_name}:')  # Print class name

        method_match = self.method_pattern.search(line)
        if method_match:
            method_name = method_match.group(1)
            method_params = method_match.group(2)
            if not self.current_class:
                self.current_class = "<global>"
                self.methods[self.current_class] = {}
            if self.current_method != method_name:
                self.current_method = method_name
                self.methods[self.current_class][self.current_method] = {'params': method_params, 'calls': []}
                print(f'\tdef {method_name}({method_params}):')  # Print method signature

        call_match = self.call_pattern.findall(line)
        if call_match and self.current_method:
            for call in call_match:
                print(f'\t\t{call[0]}({call[1]})')
                self.methods[self.current_class][self.current_method]['calls'].append(call)

        return_match = self.return_pattern.search(line)  # Check for return statement
        if return_match and self.current_method:
            print(f'\t\treturn {return_match.group(1)}')  # Print return statement
            print() # Print a new line

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        with open(file_path, 'r') as file:
            code = file.read()
            if '--import' in sys.argv:
                find_imports(code)
                generate_dependency_graph(code)
            elif '--verbose' in sys.argv:
                find_imports(code)

                # Initialize the parser
                parser = CodeParser()

                # Parse the code line by line
                for line in code.split('\n'):
                    parser.parse_line(line)
            else:
                generate_dependency_graph(code)
    else:
        print("no file path provided.")

# Example usage

# from command line

# python skeleton.py C:\Users\sidha\projects\project-intelligence\skeleton.py --verbose

# Your code snippet goes here
# code = """
# from PIL import Image
# import requests
# from mss import mss
# from io import BytesIO
# import tiktoken

# class FunctionVisitor(ast.NodeVisitor):
#         def __init__(self):
#             self.current_function = None
#             self.function_calls = {}

#         def visit_FunctionDef(self, node):
#             self.current_function = node.name
#             self.function_calls[self.current_function] = []
#             self.generic_visit(node)
#             self.current_function = None

#         def visit_Call(self, node):
#             if isinstance(node.func, ast.Name):
#                 if self.current_function:
#                     self.function_calls[self.current_function].append(node.func.id)
#             elif isinstance(node.func, ast.Attribute):
#                 if self.current_function:
#                     # This will append the method call in the format `class.method`
#                     self.function_calls[self.current_function].append(node.func.attr)
#             self.generic_visit(node)

# """

# generate_dependency_graph(code)