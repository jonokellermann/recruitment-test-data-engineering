# Data Engineering Technical Assessment Submission

## Project Overview

This project implements an ETL (Extract, Transform, Load) pipeline for processing population data. The pipeline extracts data from CSV files, processes them, loads them into a MySQL database, and finally performs an analysis to generate country population statistics. The entire solution is containerized using Docker for easy deployment and execution, with non-persistent database storage for clean runs and configuration file support for flexibility.

## Architecture

The ETL pipeline consists of four main stages:

1. **Ingestion (Extract)**: Copies CSV files from a source directory to a destination directory
2. **Process (Transform)**: Loads the CSV files into MySQL tables with basic cleaning
3. **Analysis (Load)**: Executes a SQL query to calculate population by country
4. **Orchestration**: Coordinates the execution of all pipeline stages

## Components

### Main Scripts

- `run_etl.py`: Main orchestration script that executes the entire pipeline
- `ingest.py`: Handles the data ingestion process
- `process.py`: Processes the CSV files and loads them into the database
- `analysis.py`: Executes analytical queries and saves the results to JSON

### Utility Files

- `utils/config.py`: Loads and processes configuration from YAML files with environment variable support
- `utils/constants.py`: Imports configuration settings and makes them available to other modules
- `utils/db_queries.py`: Contains SQL queries for table creation, deletion, and analysis
- `config.yaml`: Configuration file for customizing pipeline parameters

### Docker Configuration

- `docker-compose.yml`: Defines and configures the multi-container Docker application
- `Dockerfile`: (Referenced in docker-compose.yml) Defines the loader container
- `Makefile`: Provides convenient shortcuts for Docker and ETL operations

## Configuration System

The project uses a YAML-based configuration system that provides:

1. **Centralized Configuration**: All settings in one place
2. **Environment Variable Support**: Use `${VARIABLE_NAME:-default_value}` syntax to override settings with environment variables
3. **Fallback Defaults**: In case of missing configuration file or errors
4. **Separation of Concerns**: file paths, and database settings are organized in separate sections

Example configuration file:

```yaml
# Database Configuration
database:
  host: ${DATABASE_HOST:-database}
  user: ${DATABASE_USER:-codetest}
  password: ${DATABASE_PASSWORD:-swordfish}
  name: ${DATABASE_NAME:-codetest}

# File Paths
paths:
  raw_folder: /data/raw
  ingest_folder: /data/fetch
  # Additional paths...

```

## Container Infrastructure

The application is fully containerized with two main services:

1. **Database Service**:
   - Uses MySQL 8.0
   - Configured with custom authentication settings
   - Non-persistent storage for clean runs each time
   - Pre-configured database named `codetest`
   - Initialized with custom SQL setup script

2. **Loader Service**:
   - Custom built from the Dockerfile
   - Mounts source code and data directories as volumes
   - Configured with environment variables for database connection
   - Depends on the database service

## Data Flow

1. Raw CSV files containing 'people' and 'places' data are copied from `/data/raw` to `/data/fetch`
2. The pipeline connects to the MySQL database container using environment variables
3. CSV files are processed and loaded into 'people' and 'places' tables
4. A SQL query calculates population counts by country
5. Results are saved to a JSON file (`output.json`)

## Implementation Details

### Ingestion Stage

The ingestion process:
- Checks for CSV files in the source directory that contain 'people' or 'places' in their names
- Copies these files to the destination directory
- Creates metadata to track the ingestion process

### Process Stage

The process stage:
- Reads the ingested CSV files
- Performs basic data cleaning (removing duplicates)
- Loads the data into MySQL tables
- Creates metadata to track the processing status

### Analysis Stage

The analysis stage:
- Executes an SQL query that joins the 'people' and 'places' tables
- Calculates population by country (counting unique people by place of birth)
- Saves the results to a JSON file
- Creates metadata to track the analysis process

### Error Handling

Each component includes error handling to:
- Log errors
- Create metadata files with failure status when errors occur
- Check for successful completion of previous stages

### Non-Persistent Database

The database is configured with non-persistent storage, which means:
- Each run starts with a clean database state
- No data is retained between container restarts or removals
- The database is initialized using the setup.sql script on each startup
- This configuration ensures consistent and reproducible results for each ETL run

## Setup and Execution

### Prerequisites

- Docker and Docker Compose
- Git (for cloning the repository)
- Make (optional, for using the provided Makefile commands)

### Directory Structure

```
/
├── src/                # Source code directory
│   └── app/            # ETL scripts
├── utils/              # Utility modules
│   ├── config.py       # Configuration loader
│   ├── constants.py    # Configuration constants
│   └── db_queries.py   # Database queries
│   └── config.yaml     # Main configuration file
├── data/
│   ├── raw/            # Source directory for raw CSV files
│   ├── fetch/          # Destination for ingested files and metadata
│   ├── process/        # Process stage metadata
│   └── analysis/       # Analysis stage metadata and results
├── containers/
│   └── loader/
│       └── Dockerfile  # Dockerfile for the loader service
├── .docker/
│   └── setup.sql       # Database initialization script
├── docker-compose.yml  # Docker Compose configuration
└── Makefile            # Convenience commands for Docker operations
```

### Configuration Customization

To customize the ETL pipeline:

1. Edit the `config.yaml` file to change file paths, database settings, or SQL queries
2. Set environment variables to override configuration values when needed
3. For container-level changes, modify the `docker-compose.yml` file

### Running the Pipeline

#### Using Make Commands

The project includes a Makefile with convenient shortcuts:

```bash
# Start the containers in detached mode and build if necessary
make up

# Run the ETL pipeline
make run-etl

# View container logs
make logs

# Open a shell in the loader container
make sh

# Restart containers
make restart

# Stop and remove containers
make down
```

#### Using Docker Compose Directly

If you prefer not to use Make, you can use Docker Compose commands directly:

```bash
# Start the containers
docker-compose up --build -d

# Run the ETL pipeline
docker exec test-data-engineering-loader-1 python3 src/app/run_etl.py

# View logs
docker-compose logs -f
```

### Environment Variables

The following environment variables can be used to override configuration values:
- `DATABASE_HOST`: Host name of the database (default: database)
- `DATABASE_USER`: Database user name (default: codetest)
- `DATABASE_PASSWORD`: Database password (default: swordfish)
- `DATABASE_NAME`: Database name (default: codetest)

Additional environment variables can be defined in the configuration file as needed.

## Future Improvements

1. Add data validation and quality checks
2. Implement more robust error recovery mechanisms
3. Add logging to a centralized system
4. Implement parallel processing for larger datasets
5. Add unit and integration tests
6. Implement incremental loading for efficiency
7. Expand configuration options for more flexibility
8. Implement a health check for the database container before starting the ETL process
9. Add a visualization layer for the population data
10. Implement CI/CD pipeline for automated testing and deployment
11. Add option for persistent storage when needed for development purposes
