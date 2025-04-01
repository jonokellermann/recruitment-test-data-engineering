from utils.constants import (
        raw_folder_path, ingest_folder_path, ingest_metadata_file_path, 
        process_metadata_file_path, process_folder_path, 
        analysis_metadata_file_path, query_result_data_file)
from utils.db_queries import (drop_table_queries, population_query)
import ingest
import process
import os
from sqlalchemy import create_engine
import analysis
from utils.config import load_config


def main():
    try:
        config = load_config()

        ingest.perform_ingestion(raw_folder_path,ingest_folder_path, ingest_metadata_file_path)

        # Construct the MySQL connection string using config
        db_config = config['database']
        engine_str = (
            f"mysql+mysqlconnector://{db_config['user']}:"
            f"{db_config['password']}@"
            f"{db_config['host']}/"
            f"{db_config['name']}"
        )

        # Create the database engine
        engine = create_engine(engine_str)

        # Process the file
        with engine.connect() as connection:
            process.load_csv_files_to_db(
                connection,
                ingest_metadata_file_path,
                ingest_folder_path,
                process_metadata_file_path
            )
            analysis.save_query_to_json(
                connection,
                process_metadata_file_path,
                analysis_metadata_file_path,
                query_result_data_file,
                population_query)
            connection.close()

    except Exception as e:
        print(f"Error in extract process: {e}")

if __name__ == "__main__":
    main()