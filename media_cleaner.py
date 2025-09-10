import os
import shutil
import argparse
from pathlib import Path

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

def main():
    parser = argparse.ArgumentParser(description='Clean and organize media files')
    parser.add_argument('directory', help='Directory to clean and organize')
    args = parser.parse_args()
    
    target_dir = Path(args.directory)
    
    if not target_dir.exists():
        print(f"Error: Directory '{target_dir}' does not exist")
        return
    
    print(f"Cleaning directory: {target_dir}")
    
    # Process each subdirectory
    for item in target_dir.iterdir():
        if item.is_dir():
            print(f"\nProcessing: {item.name}")
            clean_directory(item)
    
    print("\nCleaning complete!")

if __name__ == "__main__":
    main()