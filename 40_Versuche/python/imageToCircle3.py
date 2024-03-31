#!/usr/bin/python

import psycopg2
from config import config
import cv2
import numpy as np
import pandas as pd

def do_image(image_name, tape_id):  # Accept tape_id as a parameter
    print(tape_id)
    tape_id -= 1
    df = process_image(image_name)
    for index, row in df.iterrows():
        insert_data(row['Radius'], row['X-coordinate'], row['Y-coordinate'], tape_id)  # Pass tape_id to insert_data
    #print(df)
    return df


def show_image_progsess(df, image, contours, radii_list, x_coords_list, y_coords_list):
    # Display DataFrame
    print(df)

    # Display the original image
    cv2.imshow('Original Image', cv2.imread(image_name))

    # Display the image with contours
    image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for contour in contours:
        cv2.drawContours(image_with_contours, [contour], 0, (0, 255, 0), 2)
    cv2.imshow('Image with Contours', image_with_contours)

    # Display the image with contours and circles
    # Create a copy of the original image for drawing circles
    image_with_circles = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    for x, y, r in zip(x_coords_list, y_coords_list, radii_list):
        cv2.circle(image_with_circles, (x, y), r, (0, 0, 255), cv2.FILLED)
    cv2.imshow('Image with Circles', image_with_circles)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def insert_data(radius, x_coordinate, y_coordinate, tape_id):
    """ Insert a new record into the database """
    sql = """INSERT INTO kreis (radius, xkooridnate, ykooridnate, tape_id) VALUES (%s, %s, %s, %s);"""
    conn = None
    try:
        # Read database configuration
        params = config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
        # Convert NumPy integers to Python integers
        radius = int(radius)
        x_coord = int(x_coordinate)
        y_coord = int(y_coordinate)
        # Execute the INSERT statement
        cur.execute(sql, (radius, x_coord, y_coord, tape_id))
        # Commit the changes to the database
        conn.commit()
        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def process_image(image_name):
    # Load the image
    image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

    # Invert the image (since blobs are black on a white background)
    image = cv2.bitwise_not(image)

    # Find contours
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Lists to store radius, x-coordinate, and y-coordinate
    radii_list = []
    x_coords_list = []
    y_coords_list = []

    # Iterate through each contour
    for contour in contours:
        # Calculate the center of gravity (centroid) and area of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            area = cv2.contourArea(contour)

            # Calculate the radius of the circle using the area
            radius = int(np.sqrt(area / np.pi))

            # Append radius, x-coordinate, and y-coordinate to respective lists
            radii_list.append(radius)
            x_coords_list.append(cx)
            y_coords_list.append(cy)

    # Create DataFrame
    data = {'Radius': radii_list, 'X-coordinate': x_coords_list, 'Y-coordinate': y_coords_list}
    df = pd.DataFrame(data)

    if __name__ == '__main__':
        show_image_progsess(df, image, contours, radii_list, x_coords_list, y_coords_list)

    return df



if __name__ == '__main__':
    image_name = 'bild1.png'

    do_image(image_name)
