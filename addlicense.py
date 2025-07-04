from fileutility import traverse_directory, read_utf8_file, safe_replace_and_prepend_header

# Load headers
previous_header_text = read_utf8_file("LICENSEHEADERPREV") or ""
new_header_text = read_utf8_file("LICENSEHEADER") or ""


def apply_latest_license_header(original_content, new_file, file_path, file_name, dir_path) -> bool:
    return safe_replace_and_prepend_header(
        original_content, new_file, file_path, new_header_text, previous_header_text)


# Traverse and process files
traverse_directory(
    "./src",
    apply_latest_license_header
)
