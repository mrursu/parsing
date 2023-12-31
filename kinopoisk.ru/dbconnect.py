import psycopg2
import psycopg2.extras
from config import host, user, password, db_name
from psycopg2.extras import execute_values
from psycopg2.extras import execute_batch
# from config import lst_data
import json




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
        # cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # cursor.execute('SELECT * FROM user_info LIMIT 5')
        
        # for record in cursor.fetchall():
        #     print(record['card'] + '\n' + record['age'])  
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    return conn

def main():
    connect()
    
if __name__ == '__main__':
    main()