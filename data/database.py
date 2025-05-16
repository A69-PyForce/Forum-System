from mariadb.connections import Connection
from dotenv import load_dotenv
from mariadb import connect
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: Must have a .env file for database connection.            #
#       Check README for instructions.                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Load environment variables from .env file
load_dotenv()
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_NAME"),
}

def _get_connection() -> Connection:
    """
    Get a database connection with credentials from DB_CONFIG.
    """
    return connect(
        user = DB_CONFIG["user"],
        password = DB_CONFIG["password"],
        host = DB_CONFIG["host"],
        port = DB_CONFIG["port"],
        database = DB_CONFIG["database"]
    )
    
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
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        return cursor.fetchall()
            
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
        cursor.execute(sql, sql_params)
        conn.commit()
        return cursor.lastrowid
            
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
        cursor.execute(sql, sql_params)
        conn.commit()
        return cursor.rowcount > 0