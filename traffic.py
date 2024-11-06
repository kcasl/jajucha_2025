import numpy as np
import cv2

def traffic_light(img_color, x, y, width, height):
    # Extract ROI from the image
    img_color = img_color[y - int(height / 2): y + int(height / 2), x - int(width / 2): x + int(width / 2)]
    
    # Convert image channel to HSV
    img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
    
    # Hyperparameters for color ranges
    lower_red_1 = (169, 40, 40)
    upper_red_1 = (179, 255, 255)
    lower_red_2 = (0, 100, 100)
    upper_red_2 = (10, 255, 255)
    lower_green = (40, 50, 50)
    upper_green = (80, 255, 255)
    
    # Mask for red colors
    img_mask_red_1 = cv2.inRange(img_hsv, lower_red_1, upper_red_1)
    img_mask_red_2 = cv2.inRange(img_hsv, lower_red_2, upper_red_2)
    img_mask_red = cv2.bitwise_or(img_mask_red_1, img_mask_red_2)
    
    # Mask for green colors
    img_mask_green = cv2.inRange(img_hsv, lower_green, upper_green)
    
    # Calculate color counts
    red_count = np.sum(img_mask_red == 255)
    green_count = np.sum(img_mask_green == 255)
    
    if red_count > 350:
        return 1  # Red detected
    elif green_count > 350:
        return 2  # Green detected
    else:
        return 0  # Neither detected

traffic_light(image,320,50,500,100)