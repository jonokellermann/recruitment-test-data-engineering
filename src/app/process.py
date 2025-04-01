import pandas as pd
import json
import os

# Process a single CSV file with batch operations
def process_csv_file(conn, file_path, table_name):
    try:
        print(f"Processing file: {file_path}")
        
        # Read CSV file (already cleaned by the load script)
        df = pd.read_csv(file_path)
        print(f"Number of rows to process: {len(df)}")
        
        #Basic clean-up
        df = df.drop_duplicates()
        df.to_sql(con=conn, name=table_name, if_exists='replace')

        print(f"Table {table_name} populated successfully")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def load_csv_files_to_db(conn, extract_metadata_file_name,ingest_folder_path, process_metadata_file_name):
    try:
        # Check if load metadata exists
        if not os.path.exists(extract_metadata_file_name):
            print("Error: Load metadata not found. Please run the load script first.")
            return False
            
        # Load The results of the previous step metadata
        with open(extract_metadata_file_name, 'r') as f:
            metadata = json.load(f)
            
        if metadata.get("status") != "completed":
            print("Error: Load process did not complete successfully.")
            return False
        
        
        # Get cleaned CSV files
        files = os.listdir(ingest_folder_path)
        fetched_csv_files = [f for f in files if f.endswith('.csv') and ('people' in f or 'places' in f)]
        
        if not fetched_csv_files:
            print("No cleaned CSV files found. Please run the load script first.")
            return False


        for filename in fetched_csv_files:
            file_path = os.path.join(ingest_folder_path, filename)
            table_name = 'people' if "people" in filename else 'places'
            process_csv_file(conn, file_path, table_name)
        
        # Save process metadata for the analysis script
        process_metadata = {
            "status": "completed",
            "tables_processed": len(fetched_csv_files),
            "table_names": fetched_csv_files
        }
        with open(process_metadata_file_name, 'w') as f:
            json.dump(process_metadata, f, indent=4)
            
        print("Process stage completed successfully")
        return True
        
    except Exception as e:
        print(f"Error in process function: {e}")
        with open(os.path.join(process_metadata_file_name), 'w') as f:
            json.dump({"status": "failed", "error": str(e)}, f, indent=4)
