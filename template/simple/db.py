import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect( 
            host="localhost", # database host ip
            user="root", # database user
            password=None, # database password
            database="test_db" # database name
        )
        return conn
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
    
def fetch_products(search=None, sort=None):
    conn = create_connection()
    if not conn:
        return []
    
    # Return the table as a dictionaries
    cursor = conn.cursor(dictionary=True)
    
    # Generate SQL request
    filters = []
    query = "SELECT * FROM products"
    
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