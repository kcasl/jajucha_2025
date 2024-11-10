import numpy as np
import cv2

def traffic_light(img_color, x, y, width, height):
    # Extract ROI from the image
    img_color = img_color[y - int(height / 2): y + int(height / 2), x - int(width / 2): x + int(width / 2)]
    
    # Convert image channel to HSV
    img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
    
    # Hyperparameters for color ranges
    lower_red_1 = (255, 182, 193)
    upper_red_1 = (255, 204, 204)
    lower_red_2 = (0, 100, 100)
    upper_red_2 = (10, 255, 255)
    lower_green = (40, 50, 50)
    upper_green = (80, 255, 255)
    lower_blue = (10, 60, 60)
    upper_blue = (61, 255, 255)
    
    Lower: (255, 182, 193)
Upper: (255, 204, 204)
    # Mask for red colors
    img_mask_red_1 = cv2.inRange(img_hsv, lower_red_1, upper_red_1)
    img_mask_red_2 = cv2.inRange(img_hsv, lower_red_2, upper_red_2)
    img_mask_red = cv2.bitwise_or(img_mask_red_1, img_mask_red_2)
    img_mask_blue = cv2.bitwise_or(img_hsv, lower_blue, upper_blue)
    img_mask_green = cv2.inRange(img_hsv, lower_green, upper_green)
    
    # Calculate color counts
    red_count = np.sum(img_mask_red == 255)
    green_count = np.sum(img_mask_green == 255)
    blue_count = np.sum(img_mask_blue == 255)
    
    return red_count, green_count, blue_count



import jajucha2
import time 


while True:

    image = jajucha2.camera.get_image('center')
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)

    Red, Green, Blue = traffic_light(image,320,50,500,100)
    right_arm = 0
    left_arm = 0
    velocity = 3
    
    print(Red, Green, Blue)

    if Red > 450:
        if Green >= 70:
            right_arm = 0
            left_arm = 0
            velocity = 3
            jajucha2.control.set_motor(left_arm, right_arm, velocity)
            time.sleep(2)
            right_arm = -9
            left_arm = -9
            velocity = 5
            jajucha2.control.set_motor(left_arm, right_arm, velocity)
            time.sleep(2)
            right_arm = 0
            left_arm = 0
            velocity = 2
            jajucha2.control.set_motor(left_arm, right_arm, velocity)
            time.sleep(1)
            jajucha2.control.stop_motor()
            break
        else:
            jajucha2.control.stop_motor()
            break

    elif Green > 170:
        if Red > 300:
            right_arm = 0
            left_arm = 0
            velocity = 3
            jajucha2.control.set_motor(left_arm, right_arm, velocity)
            time.sleep(2)
            right_arm = -9
            left_arm = -9
            velocity = 5
            jajucha2.control.set_motor(left_arm, right_arm, velocity)
            time.sleep(2.3)
            right_arm = 0
            left_arm = 0
            velocity = 2
            jajucha2.control.set_motor(left_arm, right_arm, velocity)
            time.sleep(1)
            jajucha2.control.stop_motor()
            break
        else:
            right_arm = 0
            left_arm = 0
            velocity = 6
            jajucha2.control.set_motor(left_arm, right_arm, velocity)
            time.sleep(3)
            jajucha2.control.stop_motor()
            break

    jajucha2.control.set_motor(left_arm, right_arm, velocity)
    
