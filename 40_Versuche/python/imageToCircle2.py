import cv2
import numpy as np

# Image name
image_name = 'bild1.png'

# Load the image
image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)

# Invert the image (since blobs are black on a white background)
image = cv2.bitwise_not(image)

# Find contours
contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a blank canvas with the same dimensions as the original image
contour_image = np.zeros_like(image)

# Draw contours onto the blank canvas
cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 1)

# Create a copy of the original image for drawing circles
image_with_circles = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

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
        
        # Draw a circle with the same center of gravity and area
        cv2.circle(image_with_circles, (cx, cy), radius, (0, 0, 255), -1)

# Display the image with contours and circles
cv2.imshow('Contours and Circles', image_with_circles)
cv2.waitKey(0)
cv2.destroyAllWindows()
