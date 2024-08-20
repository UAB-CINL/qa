#!/bin/bash
# Specify directory with zipped data
ZIPS="/home/wrw/prisma-qa-fates-data"
# Loop through each zip file in the directory
for zip in "$ZIPS"/*.zip; do
    # Check if the file is a zip file
    if [[ -f "$zip" ]]; then
        # Determine the directory name by removing the '.zip' extension
        DIR="${zip%.zip}"
        # Check if the directory already exists
        if [[ -d "$DIR" ]]; then
            echo "Directory $DIR already exists, skipping $zip"
        else
            # Create the directory
            mkdir -p "$DIR"
            # Unzip the file into the directory
            unzip -q "$zip" -d "$DIR"
            echo "Unzipped $zip into $DIR/"
            #TODO simplify directory structure
            #TODO heudiconv conversion
            #DCM="$ZIPS"/"$DIR"/"$DIR"/
        fi
    fi
done