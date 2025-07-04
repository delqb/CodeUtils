from io import TextIOWrapper
from fileutility import traverse_directory


def fix_imports(original_content: str, new_file: TextIOWrapper, file_path, file_name, dir_path) -> bool:
    """
    Processes the string content of a file and writes the modified content to a new file.

    - Only lines starting with 'import' (after stripping leading whitespace) are modified.
    - In those lines, '.js' is inserted before the last double quote (").
    - All lines (modified or not) are written to the new_file object.
    Returns True if the changes should persist and False if they should be discarded.
    """
    lines = original_content.splitlines(
        keepends=True)  # keep line endings intact
    has_changed = False
    line_count = 0

    for original_line in lines:
        stripped_line = original_line.lstrip()

        if not stripped_line.startswith("import") and not stripped_line.startswith("export"):
            new_file.write(original_line)
            continue

        last_double = original_line.rfind('"')
        last_single = original_line.rfind("'")
        last_quote_index = max(last_double, last_single)

        if last_quote_index == -1:
            new_file.write(original_line)
            continue

        if ".js" in stripped_line:
            new_file.write(original_line)
            continue

        line_count += 1
        # Insert '.js' before the last quote
        modified_line = original_line[:last_quote_index] + \
            '.js' + original_line[last_quote_index:]
        new_file.write(modified_line)
        has_changed = True

    print(
        f"Processed:\t{file_path} ({line_count} lines)"
        if has_changed else
        f"Skipped:\t{file_path}"
    )
    return has_changed


# Traverse and process files
traverse_directory(
    "./src",
    fix_imports
)
