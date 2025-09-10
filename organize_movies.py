import os
import re
import shutil


def clean_movie_name(filename):
    # Remove the file extension
    name, _ = os.path.splitext(filename)
    
    # Replace dots or underscores with spaces
    name = re.sub(r'[._]', ' ', name)
    
    # Remove unnecessary details (resolution, codec, etc.)
    name = re.sub(r'\b(1080p|720p|HDRip|HEVC|H265|x264|BluRay|WEBRip|HC|5\.1|BONE)\b', '', name, flags=re.IGNORECASE)
    
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Extract only name and year (if available)
    match = re.match(r'(.*?)(\s\d{4})', name)
    if match:
        name = match.group(1) + match.group(2)  # Name and year
    else:
        # Remove everything after the first non-alphabetic group
        name = re.sub(r'[^a-zA-Z0-9\s]+.*$', '', name)
    
    return name.strip()

def organize_movie_files(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        
        if os.path.isfile(file_path):
            # Clean the movie name
            cleaned_name = clean_movie_name(file)
            
            # Create a folder with the cleaned name
            folder_path = os.path.join(directory, cleaned_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            # Move the file into the folder
            new_file_path = os.path.join(folder_path, file)
            shutil.move(file_path, new_file_path)
            print(f'Moved: "{file}" -> "{new_file_path}"')

if __name__ == "__main__":
    directory = input("Enter the directory containing movie files: ").strip()
    if os.path.isdir(directory):
        organize_movie_files(directory)
    else:
        print(f'Error: "{directory}" is not a valid directory.')

