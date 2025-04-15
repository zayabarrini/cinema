import os
import re


def format_folder_name(name):
    # Replace dots or underscores with spaces
    name = re.sub(r'[._]', ' ', name)
    
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Keep only the name and the year (if available)
    match = re.match(r'(.*?)(\s\d{4})', name)
    if match:
        name = match.group(1) + match.group(2)  # Name and year
    else:
        # Remove everything after the first non-alphabetic group
        name = re.sub(r'[^a-zA-Z0-9\s]+.*$', '', name)
    
    return name.strip()

def clean_folder_names(directory):
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if os.path.isdir(folder_path):
            formatted_name = format_folder_name(folder)
            if formatted_name != folder:
                new_path = os.path.join(directory, formatted_name)
                os.rename(folder_path, new_path)
                print(f'Renamed: "{folder}" -> "{formatted_name}"')
            else:
                print(f'Skipped: "{folder}" (already formatted)')

if __name__ == "__main__":
    directory = input("Enter the directory containing movie folders: ").strip()
    if os.path.isdir(directory):
        clean_folder_names(directory)
    else:
        print(f'Error: "{directory}" is not a valid directory.')

