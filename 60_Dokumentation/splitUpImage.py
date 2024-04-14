#!/usr/bin/python

import psycopg2
from config import config
import cv2
import numpy as np
import pandas as pd
from imageToCircle3 import do_image
# Function to retrieve the last inserted tape_id
def get_last_Measurment_id(cur):

    """
    Retrieve the last inserted Measurment_id from the database.

    Args:
        cur (psycopg2.cursor): Cursor object for database interaction.

    Returns:
        int: The last inserted Measurment_id incremented by 1.
    """
    cur.execute("SELECT id FROM Measurment")
    last_Measurment_id = cur.fetchone()
    if last_Measurment_id:
        return last_Measurment_id[0] + 1
    else:
        return 1
def insert_data(MeasurmentSeries_id):
    """
    Insert a new messung entry into the database.

    Args:
        MeasurmentSeires_id (int): The ID of the MeasurmentSeries associated with the Measurment.

    Returns:
        None
    """
    sql = """INSERT INTO Measurment (MeasurmentSeries_id) 
             VALUES (%s);"""
    conn = None
    try:
        # Read database configuration
        params = config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
        # Execute the INSERT statement
        cur.execute(sql, (MeasurmentSeries_id))
        # Commit the changes to the database
        conn.commit()
        print("Messung inserted into the database.")
        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# Main function
def main():
    """
    Main function to execute the program.
    
    Prompts the user for a messungReihe ID input, processes a list of image names, and performs database operations.
    """
    # Prompt user for messung_id input
    messung_id = input("Enter MeasurmentSeries ID: ")

    # List of image names
    image_names = ['bild1.png', 'bild2.png', 'bild3.png']


    try:
                    # Read database configuration
        params = config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
    
        # Retrieve the last inserted tape_id
        messung_id = get_last_Measurment_id(cur)
        print("Next Measurment_id:", Measurment_id)

        avg_mean_radius = 0
        # Process each image
        for idx, image_name in enumerate(image_names):
            # Process the image
            avg_mean_radius += do_image(image_name, messung_id)
        avg_mean_radius = avg_mean_radius / 3

        # Commit the transaction
        conn.commit()

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
