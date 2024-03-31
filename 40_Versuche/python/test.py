#!/usr/bin/python

import psycopg2
from config import config

# Function to retrieve the last inserted tape_id
def get_last_tape_id(cur):
    cur.execute("SELECT id FROM tape")
    last_tape_id = cur.fetchone()
    if last_tape_id:
        return last_tape_id[0] + 1
    else:
        return 1

def main():
    try:
        # Read database configuration
        params = config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()

        # Retrieve the last inserted tape_id
        tape_id = get_last_tape_id(cur)
        print("Next tape_id:", tape_id)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        # Close cursor and connection
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Entry point of the program
if __name__ == "__main__":
    main()
