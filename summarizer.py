import sys

def load_code_from_file(file_path):
    """
    Loads the content of a file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

def simple_code_summarizer(script_text):
    """
    Creates a simple English summary of a Python script.
    """
    lines = script_text.splitlines()
    functions = []
    classes = []
    comments = []
    imports = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("def "):
            functions.append(stripped)
        elif stripped.startswith("class "):
            classes.append(stripped)
        elif stripped.startswith("#"):
            comments.append(stripped.lstrip("# ").strip())
        elif stripped.startswith("import ") or stripped.startswith("from "):
            imports.append(stripped)
    
    summary_parts = []

    # Note imported modules
    if imports:
        imported_names = []
        for imp in imports:
            name = ""
            if imp.startswith("import "):
                name = imp.split()[1]
            elif imp.startswith("from "):
                try:
                    name = imp.split()[1]
                except:
                    name = imp
            imported_names.append(name)
        summary_parts.append(f"This script imports {', '.join(imported_names)} and possibly other modules.")

    # Describe classes
    if classes:
        class_names = [cls.split()[1].rstrip(":") for cls in classes]
        summary_parts.append(
            f"It defines {len(classes)} class{'es' if len(classes)>1 else ''}: {', '.join(class_names)}."
        )

    # Describe functions
    if functions:
        func_names = [fn[4:].split("(")[0] for fn in functions]
        summary_parts.append(
            f"There are {len(functions)} function{'s' if len(functions)>1 else ''} defined, such as {', '.join(func_names)}."
        )
    
    # Mention main comments if present
    if comments:
        notes = " ".join(comments[:2])  # At most two main comments
        summary_parts.append(f"Comments in the code mention: {notes}")

    # If there's very little structure
    if not (imports or classes or functions):
        summary_parts.append("The script includes basic code without much structure or comments.")
    
    # Final workflow statement
    summary_parts.append(
        "When run, the script executes the defined functions and classes in order, producing output or performing tasks as coded."
    )
    return " ".join(summary_parts)

if __name__ == "__main__":
    # Check if the user provided a file argument
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py <path_to_python_file>")
        print("Example: python summarizer.py test_script.py")
        sys.exit(1)

    file_path = sys.argv[1]
    code_text = load_code_from_file(file_path)

    if code_text:
        print("\nSummary of the script:\n")
        print(simple_code_summarizer(code_text))
