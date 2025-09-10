import os
import re
import shutil
import zipfile
import argparse
from pathlib import Path
import subprocess

def clean_movie_name(filename):
    """Clean movie filename by removing unnecessary details and format as Year-Movie-Name"""
    # Remove the file extension
    name, _ = os.path.splitext(filename)
    
    # Remove common prefixes and suffixes
    name = re.sub(r'^\[[^\]]+\]\s*-\s*', '', name)  # Remove [www.UsaBit.com] - type prefixes
    name = re.sub(r'\[[^\]]+\]$', '', name)  # Remove [N1C] type suffixes
    name = re.sub(r'\([^\)]+\)$', '', name)  # Remove (ESub-Masti) type suffixes
    
    # Replace dots or underscores with spaces
    name = re.sub(r'[._]', ' ', name)
    
    # Remove technical details (resolution, codec, etc.)
    patterns = [
        r'\b(1080p|720p|480p|2160p|4K|HDRip|DVDRip|BRRip|BDRip|BluRay|Blu-Ray|WEBRip|WEB-DL|HDTV|HEVC|H265|x264|XviD|AAC|AC3|5\.1|DTS|DD5\.1|10bit|6CH|BONE|INTERNAL|iNTERNAL)\b',
        r'\b(Eng|Hindi|French|Spanish|German|Italian|Russian|Chinese|Japanese|Korean|Sub|ESub|Dubbed|Multi-Audio)\b',
        r'\b(anoXmous|MANiC|PLAYNOW|PSA|YIFY|ETRG|RARBG|AMZN|GalaxyRG|sujaidr|pimprg|QRips|RBG|WORLD|ETRG|PSA)\b',
        r'\b(Unrated|Extended|Director\'s Cut|Theatrical Cut|Final Cut|Remastered|Special Edition)\b',
        r'\[.*?\]',  # Remove anything in brackets
        r'\(.*?\)',  # Remove anything in parentheses (but be careful with years)
    ]
    
    for pattern in patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
    
    # Extract year (from various formats)
    year = None
    year_patterns = [
        r'\b(19\d{2}|20\d{2})\b',  # Standalone year (1900-2099)
        r'\((\d{4})\)',  # Year in parentheses
    ]
    
    for pattern in year_patterns:
        match = re.search(pattern, name)
        if match:
            year = match.group(1) if len(match.groups()) > 0 else match.group(0)
            name = re.sub(pattern, '', name)  # Remove the year from the name
            break
    
    # Clean up the movie name
    name = re.sub(r'[^\w\s]', '', name)  # Remove special characters but keep letters, numbers, spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Remove author/director names and other metadata
    name = re.sub(r'\b(?:by|directed by|dir|featuring|starring|with|paul|muni|luise|rainer|chantal|akerman|luis|bunuel)\b', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Replace spaces with hyphens for the final format
    name = re.sub(r'\s+', '-', name)
    
    # Format as Year-Movie-Name or just Movie-Name if no year found
    if year:
        return f"{year}-{name}"
    else:
        return name

def organize_movie_files(directory):
    """Organize movie files into folders"""
    print("Organizing movie files into folders...")
    directory = Path(directory)
    
    for file in directory.iterdir():
        if file.is_file():
            # Clean the movie name
            cleaned_name = clean_movie_name(file.name)
            
            # Create a folder with the cleaned name
            folder_path = directory / cleaned_name
            if not folder_path.exists():
                folder_path.mkdir()
            
            # Move the file into the folder
            new_file_path = folder_path / file.name
            shutil.move(str(file), str(new_file_path))
            print(f'Moved: "{file.name}" -> "{new_file_path}"')

def format_folder_name(name):
    """Format folder names to 'Year MovieName' format"""
    # Replace dots or underscores with spaces
    name = re.sub(r'[._]', ' ', name)
    
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Extract name and year (if available)
    match = re.match(r'(.*?)(\s(\d{4}))', name)
    if match:
        # If year is found, format as "Year MovieName"
        movie_name = match.group(1).strip()
        year = match.group(3)
        name = f"{year} {movie_name}"
    else:
        # Remove everything after the first non-alphabetic group
        name = re.sub(r'[^a-zA-Z0-9\s]+.*$', '', name).strip()
    
    return name

def clean_folder_names(directory):
    """Clean and standardize folder names"""
    print("Cleaning folder names...")
    directory = Path(directory)
    
    for folder in directory.iterdir():
        if folder.is_dir():
            formatted_name = format_folder_name(folder.name)
            if formatted_name != folder.name:
                new_path = directory / formatted_name
                # Handle naming conflicts
                counter = 1
                while new_path.exists():
                    new_path = directory / f"{formatted_name}_{counter}"
                    counter += 1
                
                folder.rename(new_path)
                print(f'Renamed: "{folder.name}" -> "{new_path.name}"')

def is_video_file(file_path):
    """Check if file is a video file"""
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
    return file_path.suffix.lower() in video_extensions

def is_subtitle_file(file_path):
    """Check if file is a subtitle file"""
    subtitle_extensions = {'.srt', '.ass', '.ssa', '.sub', '.idx'}
    return file_path.suffix.lower() in subtitle_extensions

def should_delete_file(file_path):
    """Check if file should be deleted (not video or subtitle)"""
    return not (is_video_file(file_path) or is_subtitle_file(file_path))

def move_subtitles_up(directory):
    """Move subtitle files from subdirectories to the main directory"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = Path(root) / file
            if is_subtitle_file(file_path) and file_path.parent != directory:
                # Move subtitle file to the main directory
                new_path = directory / file
                # Handle naming conflicts
                counter = 1
                while new_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    new_path = directory / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(new_path))
                print(f"Moved subtitle: {file_path} -> {new_path}")

def clean_directory(directory):
    """Clean and organize a single directory"""
    directory = Path(directory)
    
    # First, move any subtitles from subdirectories up
    move_subtitles_up(directory)
    
    # Remove unwanted files
    for item in directory.iterdir():
        if item.is_file() and should_delete_file(item):
            try:
                item.unlink()
                print(f"Deleted: {item}")
            except Exception as e:
                print(f"Error deleting {item}: {e}")
    
    # Remove empty subdirectories
    for item in directory.iterdir():
        if item.is_dir():
            try:
                item.rmdir()  # Will only remove if empty
                print(f"Removed empty directory: {item}")
            except OSError:
                # Directory not empty, which is fine since we might have nested structures
                pass

def get_subtitles(directory):
    """Collect all subtitle files and create a zip archive"""
    print("Collecting subtitle files...")
    directory = Path(directory)
    temp_subtitles = directory / "temp_subtitles"
    all_subtitles_zip = directory / "all_subtitles.zip"
    
    # Clean up any previous files
    if all_subtitles_zip.exists():
        all_subtitles_zip.unlink()
    
    if temp_subtitles.exists():
        shutil.rmtree(temp_subtitles)
    
    temp_subtitles.mkdir()
    
    # Process each movie folder
    for folder in directory.iterdir():
        if folder.is_dir():
            print(f"Processing: {folder.name}")
            
            # Convert folder name to filename format (spaces to hyphens)
            clean_name = folder.name.replace(' ', '-')
            
            # Find all subtitle files
            subtitle_files = []
            for ext in ['.srt', '.ass', '.ssa', '.sub', '.idx']:
                subtitle_files.extend(list(folder.glob(f"*{ext}")))
            
            if subtitle_files:
                if len(subtitle_files) == 1:
                    # Single subtitle file
                    new_name = f"{clean_name}{subtitle_files[0].suffix}"
                    dest_path = temp_subtitles / new_name
                    shutil.copy2(subtitle_files[0], dest_path)
                    print(f"  Prepared: {new_name}")
                else:
                    # Multiple subtitle files
                    counter = 1
                    for subtitle_file in subtitle_files:
                        new_name = f"{clean_name}-{counter}{subtitle_file.suffix}"
                        dest_path = temp_subtitles / new_name
                        shutil.copy2(subtitle_file, dest_path)
                        print(f"  Prepared: {new_name}")
                        counter += 1
            else:
                print(f"  No subtitle files found")
    
    # Create zip from temporary directory
    if any(temp_subtitles.iterdir()):
        with zipfile.ZipFile(all_subtitles_zip, 'w') as zipf:
            for file in temp_subtitles.iterdir():
                zipf.write(file, file.name)
        print(f"Zip file created: {all_subtitles_zip}")
    else:
        print("No subtitle files found to zip")
    
    # Clean up temporary directory
    shutil.rmtree(temp_subtitles)

def main():
    parser = argparse.ArgumentParser(description='Complete media organization and cleanup')
    parser.add_argument('directory', help='Directory containing media files')
    parser.add_argument('--skip-subtitles', action='store_true', help='Skip subtitle collection')
    args = parser.parse_args()
    
    target_dir = Path(args.directory)
    
    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' does not exist")
        return
    
    print(f"Starting media organization process for: {target_dir}")
    
    # Step 1: Organize files into folders
    organize_movie_files(target_dir)
    print("\n" + "="*50 + "\n")
    
    # Step 2: Clean folder names
    clean_folder_names(target_dir)
    print("\n" + "="*50 + "\n")
    
    # Step 3: Clean each directory (remove unwanted files, move subtitles up)
    for item in target_dir.iterdir():
        if item.is_dir():
            print(f"Cleaning directory: {item.name}")
            clean_directory(item)
    print("\n" + "="*50 + "\n")
    
    # Step 4: Collect subtitles (unless skipped)
    if not args.skip_subtitles:
        get_subtitles(target_dir)
        print("\n" + "="*50 + "\n")
    
    print("Media organization complete!")

if __name__ == "__main__":
    main()