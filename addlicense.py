import os
from fileutility import traverse_directory, read_utf8_file, safe_replace_and_prepend_header
import sys

# Load headers
previous_header_text = read_utf8_file("LICENSEHEADERPREV") or ""
new_header_text = read_utf8_file("LICENSEHEADER") or ""


def apply_latest_license_header(original_content, new_file, file_path, file_name, dir_path) -> bool:
    return safe_replace_and_prepend_header(
        original_content, new_file, file_path, new_header_text, previous_header_text)


def chooseDefault(dir_path):
    while True:
        choice = input(f"Default to '{dir_path}'? (Y/N) ").strip().lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        print("Invalid input. Please enter 'Y' or 'N'.")


def main():
    dir_path = os.path.join('.', 'src')

    if len(sys.argv) > 1:
        argument = sys.argv[1]
        if os.path.isdir(argument):
            dir_path = argument
            print(f"Using '{argument}' as the target directory.")
        else:
            print(f"'{argument}' is not a valid directory.")
            sys.exit(1)
    else:
        print(f"A target directory was not provided.")
        if not chooseDefault(dir_path):
            print(f"Exiting...")
            sys.exit(1)

    traverse_directory(
        dir_path,
        apply_latest_license_header
    )


if __name__ == "__main__":
    main()
