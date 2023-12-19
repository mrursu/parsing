import psycopg2
from config import host, user, password, db_name
from psycopg2.extras import execute_values
from psycopg2.extras import execute_batch
# from config import lst_data
from test import a
import json

def insert_data(lst): 
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """INSERT INTO user_info(card,age) VALUES (%(product_name)s, %(product_href)s)"""

        execute_batch(cursor, query,)

        conn.commit()
        
        print("[INFO] Data was succefully inserted")
        
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("[INFO] PostgreSQL connection closed")





def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    return conn

def main():
    connect()
    
if __name__ == '__main__':
    main()