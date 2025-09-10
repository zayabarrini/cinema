#!/bin/bash

# Clean up any previous files
rm -f all_subtitles.zip
rm -rf temp_subtitles
mkdir temp_subtitles

# Process each movie folder
for folder in */; do
    folder_name="${folder%/}"
    echo "Processing: $folder_name"
    
    # Convert folder name to filename format (spaces to hyphens)
    clean_name=$(echo "$folder_name" | tr ' ' '-')
    
    # Find all SRT files
    srt_files=($(find "$folder_name" -maxdepth 1 -name "*.srt"))
    
    if [ ${#srt_files[@]} -gt 0 ]; then
        if [ ${#srt_files[@]} -eq 1 ]; then
            # Single SRT file
            new_name="$clean_name.srt"
            cp "${srt_files[0]}" "temp_subtitles/$new_name"
            mv "${srt_files[0]}" "$folder_name/$new_name"
            echo "  Prepared: $new_name"
        else
            # Multiple SRT files
            counter=1
            for srt_file in "${srt_files[@]}"; do
                new_name="$clean_name-$counter.srt"
                cp "$srt_file" "temp_subtitles/$new_name"
                mv "$srt_file" "$folder_name/$new_name"
                echo "  Prepared: $new_name"
                ((counter++))
            done
        fi
    else
        echo "  No SRT files found"
    fi
done

# Create zip from temporary directory
cd temp_subtitles && zip -q ../all_subtitles.zip *.srt && cd ..
rm -rf temp_subtitles

echo "Zip file created: all_subtitles.zip with proper filenames"