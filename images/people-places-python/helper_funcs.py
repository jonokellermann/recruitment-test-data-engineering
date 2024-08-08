"""Module containing helper functions."""
import logging
import sqlalchemy
from sqlalchemy import text

# creating the logger object
logger = logging.getLogger()
# configuring the logger to info log levek
logging.basicConfig(level=logging.INFO)


def create_table_object_from_sql_script(
    schema_sql_path, table_name, connection, metadata, engine
):
    """Create a table object in a mySQL database from a sql script.

    Args:
        schema_sql_path (str): A path to the sql script that creates table
        table_name (str): The name of the table
        connection (sqlalchemy.engine.Connection): A SQLAlchemy connection object
        metadata (sqlalchemy.schema.MetaData): Metadata object
        engine (sqlalchemy.engine.Engine): Engine object

    Returns:
        sqlalchemy.schema.Table
    """
    # Create two tables: people and places by running this sql script
    with open(schema_sql_path) as file:
        query = text(file.read())
        connection.execute(query)

    # make an ORM object to refer to the table
    logging.info(f"Creating table object for '{table_name}'")
    table_obj = sqlalchemy.schema.Table(
        table_name, metadata, autoload=True, autoload_with=engine
    )
    return table_obj


def insert_df_into_table(df, table, table_name, connection):
    """Insert data from a Pandas dataframe into MySQL database table.

    Args:
      df (PandasDF): A Pandas dataframe of the data
      table (sqlalchemy.schema.Table): A ORM object of the table
      table_name (str): The name of the table
      connection (sqlalchemy.engine.Connection): A SQLAlchemy connection object
    Returns:
      None
    """
    if len(df) == 0:
        raise ValueError("Dataframe is empty. Nothing to insert")

    logging.info(f"Inserting data into table '{table_name}'")
    for index, row in df.iterrows():
        data = {column: row[column] for column in df.columns}
        instance = table.insert().values(**data)
        try:
            connection.execute(instance)
        except Exception as ex:
            logging.info(f"Error inserting row {index}: {str(ex)}")
