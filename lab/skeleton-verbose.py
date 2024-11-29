import re

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

# Example usage

# Initialize the parser
parser = CodeParser()

# Define the code to parse
code = """
class CodeParser:
    def __init__(self):
        self.class_pattern = re.compile(r'^.*class (\w+):')
        self.method_pattern = re.compile(r'^.*def (\w+)\((.*?)\):')
        self.call_pattern = re.compile(r'\s*(\w+)\((.*?)\)')
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

                return 10
"""

# Parse the code line by line
for line in code.split('\n'):
    parser.parse_line(line)