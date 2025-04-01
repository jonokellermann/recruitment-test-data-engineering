from utils.config import load_config

# Load configuration
config = load_config()

# File paths
raw_folder_path = config['paths']['raw_folder']
ingest_folder_path = config['paths']['ingest_folder']
ingest_metadata_file_path = config['paths']['ingest_metadata']
process_metadata_file_path = config['paths']['process_metadata']
process_folder_path = config['paths']['process_folder']
analysis_metadata_file_path = config['paths']['analysis_metadata']
query_result_data_file = config['paths']['query_result']