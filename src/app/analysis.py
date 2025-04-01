import pandas as pd
import json
import os

# Generate population data
def query_db(engine, output_file,query):
    try:
        print(f"Executing query: {query}")
        
        # Execute query and load directly into a pandas DataFrame
        df = pd.read_sql(query, engine)
        
        print(f"Query returned {len(df)} rows")
        print("DataFrame created successfully:")
        print(df.head())
        
        # Check if the query returned country and population
        if 'country' not in df.columns or 'population' not in df.columns:
            raise ValueError("Query must return 'country' and 'population' columns")
        
        # Convert to dictionary containing country and population
        country_population_dict = dict(zip(df['country'], df['population']))
        
        # Save results to JSON file
        with open(output_file, 'w') as json_file:
            json.dump(country_population_dict, json_file, default=str)
        
        print(f"Population data saved to {output_file}")
    except Exception as e:
        print(f"Error generating population data: {e}")


def save_query_to_json(
        engine,
        process_metadata_file_path,
        analysis_metadata_file_path,
        query_result_data_file,
        query):
    try:
        # Check if process metadata exists
        if not os.path.exists(process_metadata_file_path):
            print("Error: process metadata not found. Please run the load script first.")
            return False
            
        # Load The results of the previous step metadata
        with open(process_metadata_file_path, 'r') as f:
            metadata = json.load(f)
            if metadata.get("status") != "completed":
                print("Error: Process step did not complete successfully.")
                return False
 
        # After loading all tables, generate the population data
        population_generated = query_db(engine, query_result_data_file, query)
            
        # Save load metadata
        load_metadata = {
            "status": "completed",
            "population_data_generated": population_generated
        }
        
        with open(analysis_metadata_file_path, 'w') as f:
            json.dump(load_metadata, f)
            
        print("Analysis process completed successfully")
        
    except Exception as e:
        print(f"Error in load process: {e}")
        
        # Save error status
        with open(analysis_metadata_file_path, 'w') as f:
            json.dump({"status": "failed", "error": str(e)}, f)

