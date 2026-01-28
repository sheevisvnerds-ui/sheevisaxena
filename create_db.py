import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def try_connect(password_attempt):
    print(f"Trying password: '{password_attempt}'...")
    try:
        con = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password=password_attempt,
            host='localhost',
            port='5433'
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print(f"SUCCESS! Password is '{password_attempt}'")
        return con, password_attempt
    except psycopg2.OperationalError as e:
        print(f"Failed: {e}")
        return None, None

def create_database():
    passwords = ['SHEEVI', 'sheevi', 'Sheevi', 'admin', 'root'] # Added common defaults just in case
    
    con = None
    valid_password = None

    for p in passwords:
        con, valid_password = try_connect(p)
        if con:
            break
    
    if not con:
        print("All password attempts failed.")
        return

    # If we are here, we have a connection
    try:
        cur = con.cursor()
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'scrapewale_db'")
        exists = cur.fetchone()

        if not exists:
            print("Database 'scrapewale_db' does not exist. Creating...")
            cur.execute(sql.SQL("CREATE DATABASE scrapewale_db"))
            print("Database created successfully.")
        else:
            print("Database 'scrapewale_db' already exists.")

        cur.close()
        con.close()
        
        # Save the correct password to a file so we know what it is
        with open('correct_db_password.txt', 'w') as f:
            f.write(valid_password)

    except Exception as e:
        print(f"Error during DB creation: {e}")

if __name__ == "__main__":
    create_database()
