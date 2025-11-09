import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

# Create connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1,
    20,
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
    database=os.getenv('DB_NAME', 'equipment_lending'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'postgres')
)

def get_db_connection():
    """Get a database connection from the pool"""
    return connection_pool.getconn()

def return_db_connection(conn):
    """Return a connection to the pool"""
    connection_pool.putconn(conn)

def query_db(query, params=None, fetch_one=False, fetch_all=False):
    """Execute a database query"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
        
        conn.commit()
        cursor.close()
        return result
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        return_db_connection(conn)

