import sys
import os
import re

VERSION = "0.0.1"
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
        instructions = basic_line.split(":")
        return "\n".join(convert_basic_to_python(instr.strip(), line_number, original_line) for instr in instructions if instr.strip())
    
    # Convert CLS
    if basic_line.upper() == "CLS":
        python_code = "os.system('cls' if os.name == 'nt' else 'clear')"
    
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
            print(f"\nProcessing INPUT line: {basic_line}")  # Debug log
            print(f"Original line: {original_line}")  # Debug log
            print(f"Line number: {line_number}")  # Debug log
            
        # Remove 'INPUT' from the start and handle the space after INPUT
        input_part = basic_line[5:].strip()
        if MODEDEBUG:
            print(f"Input part: {input_part}")  # Debug log

        # Chercher d'abord une invite (texte entre guillemets)
        prompt = ""
        var = None
        
        # Chercher le texte entre guillemets
        prompt_match = re.search(r'"(.*?)"', input_part)
        if prompt_match:
            prompt = prompt_match.group(1)
            # Chercher la variable après l'invite
            remaining = input_part[prompt_match.end():].strip()
            # Chercher la variable après la virgule ou le point-virgule
            var_match = re.search(r'[,;]\s*(\w+[$%]|\w+)\s*$', remaining)
            if var_match:
                var = var_match.group(1)
            else:
                # Si pas de virgule/point-virgule, chercher la variable à la fin
                var_match = re.search(r'(\w+[$%]|\w+)\s*$', remaining)
                if var_match:
                    var = var_match.group(1)
        else:
            # Pas d'invite, chercher juste la variable
            var_match = re.search(r'(\w+[$%]|\w+)\s*$', input_part)
            if var_match:
                var = var_match.group(1)
        
        if var is None:
            if MODEDEBUG:
                print("No variable found")  # Debug log
                print(f"Failed to parse input_part: {input_part}")  # Debug log supplémentaire
            return ""
            
        if MODEDEBUG:
            print(f"Matched prompt: {prompt}, var: {var}")  # Debug log

        # Process the variable
        if "$" in var:  # String variable
            var_name = var.replace("$", "S").strip()
            python_code = f'{var_name} = input("{prompt}")' if prompt else f"{var_name} = input()"
        elif "%" in var:  # Numeric variable
            var_name = var.replace("%", "N").strip()
            python_code = f'{var_name} = int(input("{prompt}"))' if prompt else f"{var_name} = int(input())"
        else:  # Real variable
            var_name = var.strip()
            python_code = f'{var_name} = float(input("{prompt}"))' if prompt else f"{var_name} = float(input())"
            
        if MODEDEBUG:
            print(f"Generated Python code: {python_code}")  # Debug log
    
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
        # Utiliser la ligne originale complète pour le commentaire
        comment = f"# {line_number} {basic_line}" if line_number else f"# {basic_line}"
        return f"{comment}\n{python_code}"
    return ""

def process_basic_file(file_path):
    """Process the BASIC file"""
    output_file = "ConversionResult.py"
    
    try:
        # Read the BASIC file
        with open(file_path, 'r', encoding='utf-8') as file:
            original_lines = [line.strip() for line in file.readlines()]
            print(f"Successfully read BASIC file: {file_path}")
            if MODEDEBUG:
                print("\nLines read from file:")
                for i, line in enumerate(original_lines, 1):
                    print(f"{i}: {line}")
                print()
        
        # Convert BASIC to Python
        python_code = [f"# Converted from {file_path} using Basic2Python.py V{VERSION}\n\n"]
        python_code.append("# Required for CLS equivalent\nimport os\n\n")
        
        for original_line in original_lines:
            # Extract line number and content
            line_number = None
            basic_line = original_line
            
            # Chercher le numéro de ligne au début
            match = re.match(r'^(\d+)\s+(.*)', original_line)
            if match:
                line_number = match.group(1)
                basic_line = match.group(2)
            
            converted_line = convert_basic_to_python(basic_line, line_number, original_line)
            if converted_line:
                python_code.append(converted_line + "\n")
            
        # Create the Python output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(python_code)
            
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