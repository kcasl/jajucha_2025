# 알고리즘 완료

import jajucha2
import time
import cv2
import numpy as np

def depth():
    depth = jajucha2.camera.get_depth()
    height = 240
    width = int(640/3)
    x, y = int(320/3), 240
    L_display = depth[y-int(height/2):y+int(180/2), x - int(width/2):x +int(width/2)] 
    C_display = depth[y-int(height/2):y+int(180/2), x*2-int(width/2):x*2+int(width/2)] 
    R_display = depth[y-int(height/2):y+int(180/2), x*3-int(width/2):x*3+int(width/2)] 


    R_sum = np.mean(R_display)
    C_sum = np.mean(C_display)
    L_sum = np.mean(L_display)  

    jajucha2.camera.show_image(depth, 'depth')
    return (L_sum, C_sum, R_sum)

def get_mean_of_top_20(image):
    region_size = (40,110)
    center = (200,320)
    start = (center[0]-region_size[0] // 2, center[1] - region_size[1]//2)
    end = (start[0]+region_size[0],start[1]+region_size[1])
    region = image[start[0]:end[0],start[1]:end[1]]
    top_20_values = np.partition(region.flatten(),-20)[-20:]
    return np.mean(top_20_values)

mode = "straight"
Last_mode = "straight"
contact_class = 0
special = 0
contact_count = 0

while True:
    
    d = depth()
    d_set = [d[0],d[1],d[2]]
    # 기본 정보 get
    image = jajucha2.camera.get_image('center')
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)
    
    mean_of_top_20 = get_mean_of_top_20(image)
    
    #print(mean_of_top_20)
    # V[3]을 기준으로 왼쪽 오른쪽 나눈 V값들
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
    elif 171 not in V and V[3] < 140 and V[6] < 145 and (sum(L_V_set) < sum(R_V_set)):
        mode = "R_curve"
        Last_mode = "R_curve"
    elif 171 not in V and V[3] < 140 and V[1] < 145 and (sum(L_V_set) > sum(R_V_set)):
        mode = "L_curve"
        Last_mode = "L_curve"
    elif 171 not in V and V[3] < 146 and (sum(L_V_set) < sum(R_V_set)):
        mode = "R_blank_curve"
        Last_mode = "R_blank_curve"
    elif 171 not in V and V[3] < 146 and (sum(L_V_set) > sum(R_V_set)):
        mode = "L_blank_curve"
        Last_mode = "L_blank_curve"
    
    
    # if special > 1:
    #     mode = "contact"
    # elif mean_of_top_20 >= 60 and mode != "L_curve":
    #     if contact_count >= 4:
    #         mode = "contact"
    #         contact_class += 1
    #         contact_count = 0
    #     else:
    #         contact_count += 1
    
    
    if sum(d_set) > 120:
        right_arm = 0
        left_arm = 0
        velocity = -4
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(1)
        right_arm = 6
        left_arm = 6
        velocity = 5
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(2)
        right_arm = 0
        left_arm = 0
        velocity = 4
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(1)
        Last_mode = "straight"
        mode = "straight"
        jajucha2.control.stop_motor()
        # if contact_count == 0:
        #     #model
        #     right_arm = 0
        #     left_arm = 0
        #     velocity = -4
        #     jajucha2.control.set_motor(left_arm, right_arm, velocity)
        #     time.sleep(1)
        #     right_arm = 6
        #     left_arm = 6
        #     velocity = 4
        #     jajucha2.control.set_motor(left_arm, right_arm, velocity)
        #     time.sleep(2)
        #     right_arm = -6
        #     left_arm = -6
        #     velocity = 4
        #     jajucha2.control.set_motor(left_arm, right_arm, velocity)
        #     time.sleep(2)
        #     contact_count += 1
        # elif contact_count == 1:
        #     right_arm = 0
        #     left_arm = 0
        #     velocity = -4
        #     jajucha2.control.set_motor(left_arm, right_arm, velocity)
        #     time.sleep(3)
                
    if mode == 'default': 
        mode = Last_mode
        print("default", end=' ')
    if mode == 'straight':
        if V[3] <= 167:
            left_arm = -steering
            right_arm = -steering
            velocity = 6
        else:
            left_arm = -steering
            right_arm = -steering
            velocity = 7
    elif mode == 'R_curve':
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
    
    # elif mode == "contact":
    #     if contact_class % 2 == 1:
    #         while get_mean_of_top_20(image) > 40:
    #             jajucha2.control.set_motor(-30, -30, -5)
    #             image = jajucha2.camera.get_image('center')
    #             jajucha2.camera.show_image(image)
    #         else:
    #             time.sleep(0.5)
    #             jajucha2.control.set_motor(30, 30, 7)
    #             time.sleep(0.5)
    #             mode = "default"
    #             Last_mode = "straight"
    #     else:
    #         while get_mean_of_top_20(image) > 20:
    #             image = jajucha2.camera.get_image('center')
    #             (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    #             jajucha2.camera.show_image(grid)

    #             T_center = 320 - (L[0] - R[0])
    #             steering_const = 0.09
    #             steering = (320 - T_center) * steering_const
    #             steering = int(round(steering))

    #             jajucha2.control.set_motor(steering, steering, 7)
    #         else:
    #             jajucha2.control.set_motor(-30, -30, 5)
    #             time.sleep(1.5)
    #             mode = "L_curve"
    #             Last_mode = "L_curve"
    #     image = jajucha2.camera.get_image('center')
    #     jajucha2.camera.show_image(image)
    #     continue

    # while traffic_light(resized,320,50,500,100) == 1:
    #     print("traffic")
    #     jajucha.image_send(resized,client_address)
    #     velocity = 0
    #     ml.control(left_arm, right_arm, velocity, 9)
    #     resized = jajucha.image_get(qRgb)
    #     time.sleep(0.5)
    # else:
    #     pass
    
    print(f"mode:{mode}, left_arm: {left_arm}, right_arm: {right_arm}, velocity: {velocity}")

    jajucha2.control.set_motor(left_arm, right_arm, velocity)

    mode = "default"
