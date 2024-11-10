import jajucha2
import time
import cv2

steer = 0
speed = 0
mode = "straight"
Last_mode = "straight"

while True:
    # 기본 정보 get
    image = jajucha2.camera.get_image('center')
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)
    
    # V[3]을 기준으로 왼쪽 오른쪽 나눈 V값들
    L_V_set = [V[0],V[1],V[2]]
    R_V_set = [V[4],V[5],V[6]]

    # straight - 중앙추종 
    T_center = 320 - (L[2] - R[2])
    steering_const = 0.05
    steering = (320 - T_center) * steering_const
    steering = int(round(steering))



    # curve - 곡률계산
    #왼쪽으로 돌 때의 트랙 기울기 계산
    L_V_L_grad = (V[2] - V[0]) / 160
    L_V_R_grad = (V[6] - V[4]) / 160
    
    L_V_grad_s = L_V_R_grad - L_V_L_grad
    
    
    #오른쪽으로 돌 때의 트랙 기울기 계산
    R_V_L_grad = (V[2] - V[0]) / 160
    R_V_R_grad = (V[6] - V[4]) / 160
    
    R_V_grad_s = R_V_L_grad - R_V_R_grad

    c_r_steering = 5 * R_V_grad_s
    c_l_steering = 5 * L_V_grad_s
    
    
    if V[3] == 171 and abs(((L[1] + R[1])/2 + (L[0] + R[0])/2) - 440) < 100:
        mode = "straight"
        Last_mode = "straight"
    elif 171 not in V and V[3] < 150 and (sum(L_V_set) < sum(R_V_set)):
        mode = "R_curve"
        Last_mode = "R_curve"
    elif 171 not in V and V[3] < 150 and (sum(L_V_set) > sum(R_V_set)):
        mode = "L_curve"
        Last_mode = "L_curve"
    
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
        left_arm = c_r_steering
        right_arm = c_r_steering
        velocity = 4
    elif mode == 'L_curve':
        left_arm = c_l_steering
        right_arm = c_l_steering
        velocity = 4
        
    print(f"mode:{mode}, left_arm: {left_arm}, right_arm: {right_arm}, velocity: {velocity}")

    jajucha2.control.set_motor(left_arm, right_arm, velocity)

    mode = "default"
