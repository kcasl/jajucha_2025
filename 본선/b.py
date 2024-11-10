# 알고리즘 완료

import numpy as np
import cv2
import jajucha2
import time 

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
    lower_blue = (1, 107, 187)
    upper_blue = (61, 164, 255)
    
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
    
def depth():
    depth = jajucha2.camera.get_depth()
    L_display = depth[40:160, 50:] 
    C_display = depth[40:160, 50:] 
    R_display = depth[40:160, 50:]  
    
    R_sum = np.mean(R_display)
    C_sum = np.mean(C_display)
    L_sum = np.mean(L_display)  

    jajucha2.camera.show_image(depth, 'depth')
    return (R_sum, C_sum, L_sum)

mode = "straight"
Last_mode = "straight"
special = 0
contact_count = 0
time_val = 0

val1 = 0
val2 = 0
val3 = 0

while True:
    
    d = depth()
    d_set = [d[0],d[1],d[2]]
    # 기본 정보 get
    image = jajucha2.camera.get_image('center')
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)
    s_image = traffic_light(image,155,80,160,40)

    L_V_set = [V[0],V[1],V[2]]
    R_V_set = [V[4],V[5],V[6]]

    # straight - 중앙추종 
    T_center = 320 - (L[2] - R[2])
    steering_const = 0.04
    steering = (320 - T_center) * steering_const
    steering = int(round(steering))

    if V[3] == 171 and abs(((L[1] + R[1])/2 + (L[0] + R[0])/2) - 440) < 100:
        mode = "straight"
        Last_mode = "straight"
    elif 171 not in V and V[3] < 120 and V[6] < 143 and (sum(L_V_set) < sum(R_V_set)):
        mode = "R_curve"
        Last_mode = "R_curve"
    elif 171 not in V and V[3] < 120 and V[1] < 143 and (sum(L_V_set) > sum(R_V_set)):
        mode = "L_curve"
        Last_mode = "L_curve"
    elif 171 not in V and V[3] < 144 and (sum(L_V_set) < sum(R_V_set)):
        mode = "R_blank_curve"
        Last_mode = "R_blank_curve"
    elif 171 not in V and V[3] < 144 and (sum(L_V_set) > sum(R_V_set)):
        mode = "L_blank_curve"
        Last_mode = "L_blank_curve"
    
    if sum(d_set) > 145 and contact_count == 0:
        #model
        right_arm = 0
        left_arm = 0
        velocity = -4
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(1)
        right_arm = 7
        left_arm = 7
        velocity = 4
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(1.5)
        right_arm = -10
        left_arm = -10
        velocity = 4
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(2)
        contact_count += 1
        
    elif (d[0] > 40) and (sum(d_set) > 135) and contact_count == 1:
        right_arm = 0
        left_arm = 0
        velocity = -3
        jajucha2.control.set_motor(right_arm, left_arm, velocity)
        time.sleep(2)
        # right_arm = 5
        # left_arm = 5
        # right_arm = 6
        # left_arm = 6
        # right_arm = 7
        # left_arm = 7
        velocity = 3
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(1.7)
        right_arm = 0
        left_arm = 0
        velocity = 5
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(3.2)
        right_arm = 9
        left_arm = 9
        velocity = 4
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(2)
        Last_mode = "straight"
        mode = "straight"
        contact_count += 1
    
    
    # while val3 >= 1:
    #     mode = "straight"
    #     Last_mode = "straight"
    #     image = jajucha2.camera.get_image('center')
    #     (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    #     jajucha2.camera.show_image(grid)
    #     Red, Green, Blue = traffic_light(image,155,80,160,40)
    
    #     L_V_set = [V[0],V[1],V[2]]
    #     R_V_set = [V[4],V[5],V[6]]
    
    #     # straight - 중앙추종 
    #     T_center = 320 - (L[2] - R[2])
    #     steering_const = 0.04
    #     steering = (320 - T_center) * steering_const
    #     steering = int(round(steering))

    
    #     if V[3] == 171 and abs(((L[1] + R[1])/2 + (L[0] + R[0])/2) - 440) < 100:
    #         mode = "straight"
    #         Last_mode = "straight"
    #     if V[3] <= 155:
    #         while Red >= 65:
    #             velocity = 0    
    #             jajucha2.control.set_motor(0, 0, velocity)
            
    #     if mode == 'straight':
    #         if V[3] <= 167:
    #             left_arm = -steering
    #             right_arm = -steering
    #             velocity = 4
    #         else:
    #             left_arm = -steering
    #             right_arm = -steering
    #             velocity = 5
                
    #     jajucha2.control.set_motor(left_arm, right_arm, velocity)
        
    if mode == 'default': 
        mode = Last_mode
        print("default", end=' ')
    if mode == 'straight':
        if val2 >= 1:
            val3 += 1
        if V[3] <= 167:
            left_arm = -steering
            right_arm = -steering
            velocity = 4
        else:
            left_arm = -steering
            right_arm = -steering
            velocity = 5
    elif mode == 'R_curve':
        if val1 >= 1:
            val2 +=1
        if V[3] <= 110: # and False:
            left_arm = 10
            right_arm = 10
            velocity = 5
        else:
            left_arm = 8
            right_arm = 8
            velocity = 5
    elif mode == 'L_curve':
        if V[3] <= 110: #and False
            left_arm = -10
            right_arm = -10
            velocity = 5
        else:
            left_arm = -8
            right_arm = -8
            velocity = 5
    elif mode == 'R_blank_curve':
        left_arm = 9
        right_arm = 9
        velocity = 4
    elif mode == 'L_blank_curve':
        left_arm = -9
        right_arm = -9
        velocity = 4
    
    print(time_val)
    
    jajucha2.control.set_motor(left_arm, right_arm, velocity)
    
    mode = "default"
    
