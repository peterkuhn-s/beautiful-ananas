import cv2
import numpy as np
import threading

def display_image(image):
    # Display the image
    cv2.imshow('Result', image)
    cv2.waitKey(0)  # Wait for any key press
    cv2.destroyAllWindows()

# Image name
image_name = 'bild1.png'

# Load the image
image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

# Invert the image (since blobs are black on a white background)
image = cv2.bitwise_not(image)

# Find contours
contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Minimum contour area threshold
min_contour_area = 100  # Adjust this value according to your needs

# Filter contours based on area
valid_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

print(valid_contours)

# Create a blank canvas with the same dimensions as the original image
contour_image = np.zeros_like(image)

# Draw contours onto the blank canvas
cv2.drawContours(contour_image, valid_contours, -1, (255, 255, 255), 1)

# Display the image with contours
#cv2.imshow('Contours', contour_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Iterate through each valid contour
for contour in valid_contours:
    # Calculate the center of gravity (centroid) and area of the contour
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        area = cv2.contourArea(contour)
        
        # Calculate the radius of the circle using the area
        radius = int(np.sqrt(area / np.pi))
        
        # Draw a circle with the same center of gravity and area
        cv2.circle(image, (cx, cy), radius, (0, 255, 0), -1)

# Display the result
cv2.imshow('Result', image)
cv2.waitKey(0)  # Wait for any key press
cv2.destroyAllWindows()
# Create a new thread to display the image
#display_thread = threading.Thread(target=display_image, args=(image,))
#display_thread.daemon = True  # Set as daemon thread
#display_thread.start()

# Continue with the main thread
# Any additional processing can be done here
