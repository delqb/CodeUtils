import os
from typing import Callable, TextIO


def traverse_directory(
    path: str,
    callback_fn: Callable[[str, TextIO, str, str, str], bool]
):
    def create_bk(file_path):
        bk_file_path = file_path + ".bk"
        if os.path.exists(bk_file_path):
            print(
                f"Warning: Backup file {bk_file_path} already exists. Skipping file {file_path}.")
            return None
        os.rename(file_path, bk_file_path)
        return bk_file_path

    def clear_bk(bk_file_path):
        if os.path.exists(bk_file_path):
            os.remove(bk_file_path)

    def restore_file(bk_file_path, file_path):
        if os.path.exists(bk_file_path):
            if os.path.exists(file_path):
                os.remove(file_path)
            os.rename(bk_file_path, file_path)

    found = 0
    changed = 0
    for dir_path, dir_names, file_names in os.walk(path):
        for file_name in file_names:
            apply_changes = False
            file_path = os.path.join(dir_path, file_name)

            if not os.path.isfile(file_path):
                print(f"Error occurred: {file_path} does not exist.")
                continue

            # Found file
            found += 1

            # Add .bk extension
            bk_file_path = create_bk(file_path)
            if not bk_file_path:
                continue

            # bk_file_path = file_path + ".bk"
            # if os.path.exists(bk_file_path):
            #     print(
            #         f"Warning: Backup file {bk_file_path} already exists. Skipping {file_path}.")
            #     continue

            # os.rename(file_path, bk_file_path)

            try:
                original_content = None
                with open(bk_file_path, "r", encoding="utf-8") as original_file:
                    original_content = original_file.read()

                with open(file_path, "w", encoding="utf-8") as new_file:
                    apply_changes = callback_fn(original_content, new_file,
                                                file_path, file_name, dir_path)
            except Exception as e:
                print(
                    f"Error occurred: {e}. Restoring original file.")
                apply_changes = False

            if not apply_changes:
                restore_file(bk_file_path, file_path)
                continue
            else:
                changed += 1
                clear_bk(bk_file_path)

    print(f"Found: {found}")
    print(f"Changed: {changed}")


def safe_replace_and_prepend_header(original_content: str, new_file, file_path, new_header: str, previous_header=None):
    # Remove previous header if present
    if previous_header and original_content.startswith(previous_header):
        original_content = original_content[len(previous_header):]

    # Check if new header is already present
    if original_content.startswith(new_header):
        # Restore the file as-is, no change needed
        print(f"Skipped (already has new header): {file_path}")
        return False

    # Write new header + rest of file
    new_file.write(new_header)
    new_file.write(original_content)

    print(f"Processed: {file_path}")
    return True


def read_utf8_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"{file_path} file not found.")
        return None
    except UnicodeDecodeError:
        print(f"Error decoding {file_path}. Make sure it's UTF-8 encoded.")
        return None
