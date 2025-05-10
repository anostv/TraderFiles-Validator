from Npp import *   # Import Notepad++ PythonScript API

def validate_trader_buffer():
    seen_items = set()
    duplicates = []
    invalid_lines = []

    # Read the entire text from the current editor tab, split by lines
    lines = editor.getText().splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()     # Remove leading/trailing spaces

        # Skip empty lines or full-line comments
        if not stripped or stripped.startswith("//"):
            continue

        # Skip trader/category/currency headers
        if stripped.startswith("<Trader>") or stripped.startswith("<Category>") or stripped.startswith("<Currency>"):
            continue

        # Skip other config block tags like <FileEnd>, <OpenFile>, etc.
        if stripped.startswith("<") and stripped.endswith(">"):
            continue

        # Remove inline comments: everything after //
        code_only = line.split('//')[0].strip()

        # Check if the line is a potential item line (contains commas)
        if ',' in code_only:
            comma_count = code_only.count(',')
            if comma_count != 3:
                invalid_lines.append((i + 1, line.strip(), comma_count))

            # Extract the item classname (text before the first comma)
            classname = code_only.split(',')[0].strip()
            
            # Check for duplicate item names
            if classname in seen_items:
                duplicates.append((i + 1, classname))
            else:
                seen_items.add(classname)

    console.show()
    console.clear()
    
    # Print results
    if invalid_lines or duplicates:
        console.write("Validation Failed.\n\n")
        if invalid_lines:
            console.write("Lines with wrong number of commas (should be 3):\n")
            for ln, content, count in invalid_lines:
                console.write("  Line {}: {} (commas: {})\n".format(ln, content, count))
            console.write("\n")
        if duplicates:
            console.write("Duplicate item classnames found:\n")
            for ln, classname in duplicates:
                console.write("  Line {}: {}\n".format(ln, classname))
    else:
        console.write("Validation passed: No issues found.\n")

# Run the validation when the script is executed
validate_trader_buffer()
