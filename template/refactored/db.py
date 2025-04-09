import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Create connection with the database.
    """
    
    ###### MariaDB connection info ######

    HOST = "localhost"
    USER = "root"
    PASSWORD = None # INSERT YOUR PASSWORD
    DATABASE = "test_db"

    #####################################
    
    try:
        conn = mysql.connector.connect(
            host= HOST,
            user= USER,
            password= PASSWORD,
            database= DATABASE
        )
        return conn
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def fetch_products_from_db(search=None, sort=None):
    conn = create_connection()
    if not conn:
        return []

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM products"
    filters = []

    if search:
        filters.append(f"name LIKE '%{search}%'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    if sort and (sort == "asc" or sort == "desc"):
        query += f" ORDER BY price {sort.upper()}"

    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
