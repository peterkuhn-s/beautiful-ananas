#!/usr/bin/python

import psycopg2
from config import config
import cv2
import numpy as np
import pandas as pd

def do_image(image_name, messung_id):  # Accept tape_id as a parameter
    """
    Process an image to detect circles, calculate statistics, and insert data into the database.

    Args:
        image_name (str): The filename of the image to process.
        messung_id (int): The ID of the Messung associated with the circles in the image.

    Returns:
        float: The mean radius of the detected circles.
    """
    df = process_image(image_name)
    mean_radius = perform_statistics(df, messung_id)

    tape_id = get_last_tape_id()
    for index, row in df.iterrows():
        insert_data_kreis(row['Radius'], row['X-coordinate'], row['Y-coordinate'], tape_id)  # Pass tape_id to insert_data
    #print(df)
    return mean_radius

# Function to perform statistics on a DataFrame
def perform_statistics(df, messung_id):
    """
    Calculate statistics on a DataFrame containing circle data and insert them into the database.

    Args:
        df (pandas.DataFrame): DataFrame containing circle data.
        messung_id (int): The ID of the Messung associated with the circle data.

    Returns:
        float: The mean radius of the detected circles.
    """

    # Calculate mean and standard deviation
    mean_radius = df['Radius'].mean()
    mean_x_coordinate = df['X-coordinate'].mean()
    mean_y_coordinate = df['Y-coordinate'].mean()
    std_radius = df['Radius'].std()
    std_x_coordinate = df['X-coordinate'].std()
    std_y_coordinate = df['Y-coordinate'].std()

    # Insert statistics into the database
    insert_data_tape(mean_radius, mean_x_coordinate, mean_y_coordinate, std_radius, std_x_coordinate, std_y_coordinate, messung_id)

    return mean_radius


def insert_data_tape(mean_radius, mean_x_coordinate, mean_y_coordinate, std_radius, std_x_coordinate, std_y_coordinate, messung_id):
    """
    Insert statistics into the database.

    Args:
        mean_radius (float): Mean radius of detected circles.
        mean_x_coordinate (float): Mean x-coordinate of detected circles.
        mean_y_coordinate (float): Mean y-coordinate of detected circles.
        std_radius (float): Standard deviation of radius of detected circles.
        std_x_coordinate (float): Standard deviation of x-coordinate of detected circles.
        std_y_coordinate (float): Standard deviation of y-coordinate of detected circles.
        messung_id (int): The ID of the Messung associated with the statistics.

    Returns:
        None
    """
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
def get_last_tape_id():
    """
    Retrieve the ID of the last inserted tape from the database.

    Returns:
        int: The ID of the last inserted tape.
    """
            # Read database configuration
    params = config()
        # Connect to the PostgreSQL database
    conn = psycopg2.connect(**params)
        # Create a new cursor
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM tape")
    last_tape_id = cur.fetchone()
    if last_tape_id:
        return last_tape_id[0]
    else:
        return 1



def show_image_progsess(df, image, contours, radii_list, x_coords_list, y_coords_list):
    """
    Display the processed image with circles and contours.

    Args:
        df (pandas.DataFrame): DataFrame containing circle data.
        image (numpy.ndarray): Original image.
        contours (list): List of contours detected in the image.
        radii_list (list): List of radii of detected circles.
        x_coords_list (list): List of x-coordinates of detected circles.
        y_coords_list (list): List of y-coordinates of detected circles.

    Returns:
        None
    """
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


def insert_data_kreis(radius, x_coordinate, y_coordinate, tape_id):
    """
    Insert circle data into the database.

    Args:
        radius (int): Radius of the circle.
        x_coordinate (int): X-coordinate of the circle.
        y_coordinate (int): Y-coordinate of the circle.
        tape_id (int): The ID of the tape associated with the circle.

    Returns:
        None
    """
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
    """
    Process an image to detect circles and return a DataFrame containing circle data.

    Args:
        image_name (str): The filename of the image to process.

    Returns:
        pandas.DataFrame: DataFrame containing circle data.
    """
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
