#!/usr/bin/python

import psycopg2
from config import config
import cv2
import numpy as np
import pandas as pd
from imageToCircle3 import do_image

# Function to perform statistics on a DataFrame
def perform_statistics(df, messung_id):


    # Calculate mean and standard deviation
    mean_radius = df['Radius'].mean()
    mean_x_coordinate = df['X-coordinate'].mean()
    mean_y_coordinate = df['Y-coordinate'].mean()
    std_radius = df['Radius'].std()
    std_x_coordinate = df['X-coordinate'].std()
    std_y_coordinate = df['Y-coordinate'].std()

    # Insert statistics into the database
    insert_data(mean_radius, mean_x_coordinate, mean_y_coordinate, std_radius, std_x_coordinate, std_y_coordinate, messung_id)


def insert_data(mean_radius, mean_x_coordinate, mean_y_coordinate, std_radius, std_x_coordinate, std_y_coordinate, messung_id):
    """ Insert statistics into the database """
    sql = """INSERT INTO tape (radiusmittelwert, xaxemittelwert, yaxesmittelwert, radiussd, xaxesd, yaxesd, messung_id) 
             VALUES (%s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        # Read database configuration
        params = config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
        # Execute the INSERT statement
        cur.execute(sql, (mean_radius, mean_x_coordinate, mean_y_coordinate, std_radius, std_x_coordinate, std_y_coordinate, messung_id))
        # Commit the changes to the database
        conn.commit()
        print("Statistics inserted into the database.")
        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
# Function to retrieve the last inserted tape_id
def get_last_tape_id(cur):
    cur.execute("SELECT id FROM tape")
    last_tape_id = cur.fetchone()
    if last_tape_id:
        return last_tape_id[0] + 1
    else:
        return 1

# Main function
def main():
    # Prompt user for messung_id input
    messung_id = input("Enter Messung ID: ")

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
        tape_id = get_last_tape_id(cur)
        print("Next tape_id:", tape_id)

        # Process each image
        for idx, image_name in enumerate(image_names):
            # Process the image
            df = do_image(image_name, tape_id)
            
            # Perform statistics on each DataFrame
            print("Statistics for Image", idx+1)
            perform_statistics(df, messung_id)  # Pass tape_id to perform_statistics

            # Increment tape_id for the next image
            tape_id += 1

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
