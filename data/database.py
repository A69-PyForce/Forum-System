import sys
from pathlib import Path

# Add the parent directory of 'utils' to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.console_messages import console_message
from mariadb.connections import Connection
from mariadb.connections import Connection
from mariadb import connect
import json

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: Must have a db_config.json file for database connection.  #
# If the file is missing, create it using this template:          #
#                                                                 #
# {                                                               #
#     "user": "",                                                 #
#     "password": "",                                             #
#     "host": "",                                                 #
#     "port": 0,                                                  #
#     "database": ""                                              #
# }                                                               #
#                                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Open db_config.json file.
with open ('db_config.json', 'r') as file:
    db_config = json.load(file)

def _get_connection() -> Connection:
    """
    Get a database connection with credentials from db_config.json.
    """
    return connect(
        user = db_config["user"],
        password = db_config["password"],
        host = db_config["host"],
        port = db_config["port"],
        database = db_config["database"]
    )

# Initial try to connect to Database
try:
    _ = _get_connection()
    console_message("INFO", f"Database connection on adress '{db_config["host"]}:{db_config["port"]}' successful. Using schema '{db_config["database"]}'.")

except Exception as e:
    console_message("ERROR", e)
    
def read_query(sql: str, sql_params=()) -> list[tuple]:
    """
    Read and execute a SQL query. For parameterized queries, use '?' as a placeholder \n
    for parameters and pass their values as a tuple in the sql_params argument.
    Args:
        sql (str): The SQL query string to execute.
        sql_params (tuple): The SQL query parameters. Defaults as an empty tuple.
        
    Returns:
        list: The result of the SQL query as a sequence of sequences, e.g. list(tuple).
    """
    with _get_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, sql_params)
            return cursor.fetchall()
        except Exception as e:
           console_message("ERROR", e)
            
def insert_query(sql: str, sql_params=()) -> int:
    """
    Execute an INSERT SQL query and return the ID of the last inserted row.
    
    Args:
        sql (str): The INSERT SQL query string.
        sql_params (tuple): The parameters for the query. Defaults to an empty tuple.
        
    Returns:
        int: The ID of the last inserted row.
    """
    with _get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql, sql_params)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            console_message("ERROR", e)
            
def update_query(sql: str, sql_params=()) -> bool:
    """
    Execute an UPDATE SQL query.
    
    Args:
        sql (str): The UPDATE SQL query string.
        sql_params (tuple): The parameters for the query. Defaults to an empty tuple.
        
    Returns:
        bool: True if rows were affected, False otherwise.
    """
    with _get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql, sql_params)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            console_message("ERROR", e)