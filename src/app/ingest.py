import os
import pandas as pd
import json
import shutil

def perform_ingestion(data_source_path,data_destination_path,extract_metadata_file_name):
    try:
        # Check if the directory exists
        if not os.path.exists(data_source_path):
            print(f"Error: Directory '{data_source_path}' does not exist")
            return
    
        # List files in the directory
        files = os.listdir(data_source_path)
        csv_files = [f for f in files if f.endswith('.csv') and ("people" in f or 'places' in f)]
    
        if not csv_files:
            print(f"No CSV files found in '{data_source_path}'")
            return
        
        # Save metadata about the extracted data
        metadata = {
            "file_names": csv_files,
            "status": "completed"
        }
        
        for filename in csv_files:
            new_filename = os.path.join(data_destination_path, filename)
            filepath = os.path.join(data_source_path, filename)
            shutil.copy(filepath, new_filename)
        
        # Save successful extraction
        with open(extract_metadata_file_name, 'w') as f:
            json.dump(metadata, f, indent=4)
            print("Fetch process completed successfully")
        
    except Exception as e:
        print(f"Error in extract process: {e}")
        # Save error status
        with open(extract_metadata_file_name, 'w') as f:
            json.dump({"status": "failed", "error": str(e)}, f, indent=4)
