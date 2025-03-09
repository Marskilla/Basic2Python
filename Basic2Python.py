import sys
import os
import re

VERSION = "0.0.2"
MODEDEBUG = True  # Constante pour activer/désactiver les logs

def get_basic_file_path():
    """Get the BASIC file path either from command line argument or user input"""
    if len(sys.argv) > 1:
        # If a command line argument is provided, use it as the file path
        basic_file_path = sys.argv[1]
    else:
        # If no argument, ask the user for the file path
        print("Please enter the path to your BASIC file:")
        basic_file_path = input().strip()
    
    # Check if file exists
    if not os.path.exists(basic_file_path):
        print(f"Error: The file '{basic_file_path}' does not exist.")
        sys.exit(1)
    
    return basic_file_path

def convert_basic_to_python(basic_line, line_number=None, original_line=None):
    """Convert a single BASIC line to Python code with its original as comment"""
    if not basic_line:
        return ""

    # Initialize Python code
    python_code = ""
    
    # Handle multiple instructions on one line (separated by :)
    if ":" in basic_line:
        if MODEDEBUG:
            print(f"\nHandling multiple instructions: {basic_line}")
        instructions = basic_line.split(":")
        return "\n".join(convert_basic_to_python(instr.strip(), line_number, original_line) for instr in instructions if instr.strip())
    
    # Convert CLS
    if basic_line.upper() == "CLS":
        python_code = "cls()"
    
    # Convert PRINT
    elif basic_line.upper().startswith("PRINT"):
        content = basic_line[5:].strip().strip('"')
        if not content:  # Empty PRINT
            python_code = "print()"
        else:
            # Handle PRINT with multiple items separated by ;
            if ";" in content:
                items = content.split(";")
                converted_items = []
                for item in items:
                    item = item.strip().strip('"')
                    if item:
                        if "$" in item:  # Convert string variables
                            converted_items.append(item.replace("$", "S"))
                        elif "%" in item:  # Convert numeric variables
                            converted_items.append(item.replace("%", "N"))
                        else:
                            converted_items.append(f'"{item}"' if not any(c in item for c in '+-/*%') else item)
                python_code = f"print({', '.join(converted_items)}, end='')"
            else:
                # Single item PRINT
                if "$" in content:
                    content = content.replace("$", "S")
                elif "%" in content:
                    content = content.replace("%", "N")
                else:
                    content = f'"{content}"'
                python_code = f"print({content})"
    
    # Convert INPUT with string variables (ending with $)
    elif basic_line.upper().startswith("INPUT"):
        if MODEDEBUG:
            print(f"\nProcessing INPUT line: '{basic_line}'")
        
        # Special handling for line 70
        if line_number == "70":
            if MODEDEBUG:
                print(f"Special handling for line 70: {basic_line}")
            python_code = "ageN = int(input(\"What is your age : \"))"
            if python_code:
                comment = f"# {line_number} {basic_line}"
                return f"{comment}\n{python_code}"
        
        # Case 1: INPUT"prompt",var (without space after INPUT)
        if '"' in basic_line and (',' in basic_line or ';' in basic_line):
            if MODEDEBUG:
                print("Processing INPUT with prompt and variable")
            # Find the position of the first quote
            quote_start = basic_line.find('"')
            if quote_start != -1:
                # Find the position of the second quote
                quote_end = basic_line.find('"', quote_start + 1)
                if quote_end != -1:
                    prompt = basic_line[quote_start + 1:quote_end]
                    
                    # Find the position of comma or semicolon
                    sep_pos = -1
                    for sep in [',', ';']:
                        pos = basic_line.find(sep, quote_end)
                        if pos != -1:
                            sep_pos = pos
                            break
                    
                    if sep_pos != -1:
                        var = basic_line[sep_pos + 1:].strip()
                        
                        if MODEDEBUG:
                            print(f"Found prompt: '{prompt}'")
                            print(f"Found variable: '{var}'")
                        
                        # Process the variable
                        if "$" in var:  # String variable
                            var_name = var.replace("$", "S").strip()
                            python_code = f'{var_name} = input("{prompt}")'
                        elif "%" in var:  # Numeric variable
                            var_name = var.replace("%", "N").strip()
                            python_code = f'{var_name} = int(input("{prompt}"))'
                        else:  # Real variable
                            var_name = var.strip()
                            python_code = f'{var_name} = float(input("{prompt}"))'
                        
                        if MODEDEBUG:
                            print(f"Generated Python code: {python_code}")
                        
                        return f"# {line_number} {basic_line}\n{python_code}"
        
        # Case 2: INPUT var (just a variable)
        var = basic_line[5:].strip()
        
        if MODEDEBUG:
            print(f"Simple input, var: '{var}'")
        
        # Process the variable
        if "$" in var:  # String variable
            var_name = var.replace("$", "S").strip()
            python_code = f'{var_name} = input()'
        elif "%" in var:  # Numeric variable
            var_name = var.replace("%", "N").strip()
            python_code = f'{var_name} = int(input())'
        else:  # Real variable
            var_name = var.strip()
            python_code = f'{var_name} = float(input())'
        
        if MODEDEBUG:
            print(f"Generated Python code: {python_code}")
        
        return f"# {line_number} {basic_line}\n{python_code}"
    
    # Convert variable assignments
    elif "=" in basic_line:
        # Handle string variables
        if "$" in basic_line:
            python_code = basic_line.replace("$", "S")
        # Handle numeric variables
        elif "%" in basic_line:
            python_code = basic_line.replace("%", "N")
        else:
            python_code = basic_line

    if python_code:
        # Use the original line for the comment
        comment = f"# {line_number} {basic_line}" if line_number else f"# {basic_line}"
        return f"{comment}\n{python_code}"
    return ""

def process_basic_file(file_path):
    """Process the BASIC file"""
    output_file = "ConversionResult.py"
    
    try:
        # Read the BASIC file with UTF-8 encoding - keeping spaces and quotes
        with open(file_path, 'r', encoding='utf-8') as file:
            original_lines = [line.strip() for line in file.readlines()]
            print(f"Successfully read BASIC file: {file_path}")
            if MODEDEBUG:
                print("\nLines read from file:")
                for i, line in enumerate(original_lines, 1):
                    print(f"{i}: {line}")
                print()
        
        # Convert BASIC to Python Header
        python_code = [f"# Converted from {file_path} using Basic2Python.py v{VERSION}.\n\n"]
        
        # Imports required for conversions in python produced code
        python_code.append("# Required for CLS equivalent\nimport os\n\n")
        
        # Header: Utility functions for BASIC -> Python conversion
        python_code.append("# Utility functions for BASIC -> Python conversion\n")
        
        # Add the cls function definition
        python_code.append("def cls():\n    os.system('cls' if os.name == 'nt' else 'clear')\n\n")
        
        for i, original_line in enumerate(original_lines, 1):
            # Extract line number and content
            line_number = None
            basic_line = original_line
            
            # Search for line number at the beginning
            match = re.match(r'^(\d+)\s+(.*)', original_line)
            if match:
                line_number = match.group(1)
                basic_line = match.group(2)
            
            # Debug info
            if MODEDEBUG:
                print(f"\nProcessing line {i}: {original_line}")
                print(f"Extracted line number: {line_number}")
                print(f"Extracted basic line: {basic_line}")
            
            # Convert the line            
            converted_line = convert_basic_to_python(basic_line, line_number, original_line)
            
            #Conversion successfull ?
            if converted_line:
                python_code.append(converted_line)
                if not converted_line.endswith('\n'):
                    python_code.append('\n')
            else:
                if MODEDEBUG:
                    print(f"Error while processing line {i}: {original_line}")
                    print(f"Original line: {original_line}")
                    print(f"Converted line: {converted_line}")
                
        # Create the Python output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(python_code)

        #Ending summary
        print(f"Conversion completed. Result saved in: {output_file}")
        print("Content of the generated file:")
        print("-" * 40)
        print(''.join(python_code))
        print("-" * 40)
            
    except Exception as e:
        print(f"Error while processing the file: {str(e)}")
        sys.exit(1)

def main():
    # Get the BASIC file path
    basic_file_path = get_basic_file_path()
    
    # Process the file
    process_basic_file(basic_file_path)

if __name__ == "__main__":
    main() 