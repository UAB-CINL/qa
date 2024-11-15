#!/bin/bash

# Define the folder paths
ZIP_FOLDER="/mnt/d/CINL/QA2024/scratch"
OUTPUT_FOLDER="/mnt/d/CINL/QA2024/scratch/out"
TMP_UNZIP_FOLDER="$OUTPUT_FOLDER/temp_unzip"
BIDS_OUTPUT="$OUTPUT_FOLDER/bids"

# Create necessary directories
mkdir -p "$TMP_UNZIP_FOLDER"
mkdir -p "$BIDS_OUTPUT"

# Iterate over each zip file in the folder
for zipfile in "$ZIP_FOLDER"/*.zip; do
    echo "Processing $zipfile..."
    
    # Unzip the archive into the temporary folder
    unzip -q "$zipfile" -d "$TMP_UNZIP_FOLDER"
    
    # Find the directory named "ep2d_FATES_160vols_2004bw"
    dicom_dir=$(find "$TMP_UNZIP_FOLDER" -type d -name "ep2d_FATES_160vols_2004bw" | head -n 1)
    
    if [[ -z "$dicom_dir" ]]; then
        echo "Directory 'ep2d_FATES_160vols_2004bw' not found in $zipfile. Skipping..."
        rm -rf "$TMP_UNZIP_FOLDER"/*
        continue
    fi

    echo $dicom_dir
    
    # Extract the exam name from the zip file name
    zip_basename=$(basename "$zipfile" .zip)
    
    # Use regex to extract date and study ID, handling both variations
    if [[ "$zip_basename" =~ Qa([0-9]{8})(_CINL|CINL_)?([0-9]{4})? ]]; then
        exam_date="${BASH_REMATCH[1]}"
        study_id="${BASH_REMATCH[3]:-0000}"  # Default to "0000" if missing
    elif [[ "$zip_basename" =~ ([0-9]{8})Qa(_CINL|CINL_)?([0-9]{4})? ]]; then
        exam_date="${BASH_REMATCH[1]}"
        study_id="${BASH_REMATCH[3]:-0000}"  # Default to "0000" if missing
    else
        echo "Could not parse date or study ID from $zip_basename. Skipping..."
        rm -rf "$TMP_UNZIP_FOLDER"/*
        continue
    fi
    
    # Construct standardized name
    session_name="Qa${exam_date}_CINL${study_id}"
    echo "Standardized session name: $session_name"
    
    # Move DICOM directory to the standardized name folder
    standardized_folder="$TMP_UNZIP_FOLDER/$session_name"
    mv "$dicom_dir" "$standardized_folder"
    
    # Run HeuDiConv to convert the DICOMs to BIDS
    heudiconv -s "fbirn" \
              -ss "$session_name" \
              --files "$standardized_folder" \
              -o "$BIDS_OUTPUT" \
              -f heuristic1.py \
              -c dcm2niix \
              -b \
              --overwrite
    
    # Clean up temporary folder
    rm -rf "$TMP_UNZIP_FOLDER"/*
done

echo "Conversion complete. Check $BIDS_OUTPUT for the output."
