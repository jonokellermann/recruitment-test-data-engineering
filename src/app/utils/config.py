import os
import yaml
import re

def load_config(config_path=None):
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    try:
        with open(config_path, 'r') as file:
            # Load the YAML content
            config_str = file.read()
            
            # Replace environment variables
            pattern = r'\${([^}^{]+)}'
            
            def replace_env_vars(match):
                env_var = match.group(1)
                var_name, default = env_var.split(':-') if ':-' in env_var else (env_var, '')
                return os.environ.get(var_name, default)
            
            config_str = re.sub(pattern, replace_env_vars, config_str)
            
            # Parse the YAML
            config = yaml.safe_load(config_str)
            
            return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        # Return a minimal default configuration
        return {
            "database": {
                "host": os.environ.get("DATABASE_HOST", "database"),
                "user": os.environ.get("DATABASE_USER", "codetest"),
                "password": os.environ.get("DATABASE_PASSWORD", "swordfish"),
                "name": os.environ.get("DATABASE_NAME", "codetest")
            },
            "paths": {
                "raw_folder": "/data/raw",
                "ingest_folder": "/data/fetch",
                "ingest_metadata": "/data/fetch/fetch_metadata.json",
                "process_metadata": "/data/process/process_metadata.json", 
                "process_folder": "/data/process",
                "analysis_metadata": "/data/analysis/analysis_metadata.json",
                "query_result": "output.json"
            }
        }