# 알고리즘 완료

import numpy as np
import cv2
import jajucha2
import time 
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, WeightedRandomSampler, Subset, random_split
from torchvision import datasets, models, transforms
import numpy as np
from PIL import Image

def traffic_light(img_color, x, y, width, height):
    # Extract ROI from the image
    img_color = img_color[y - int(height / 2): y + int(height / 2), x - int(width / 2): x + int(width / 2)]
    
    return img_color
    
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
special = 0
contact_count = 0
time_val = 0

val1 = 0
val2 = 0
val3 = 0

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 모델 불러오기
    base_model = models.mobilenet_v2(pretrained=False)  # 'pretrained=False'로 설정
    num_ftrs = base_model.classifier[1].in_features
    base_model.classifier = torch.nn.Sequential(
        torch.nn.Linear(num_ftrs, 128),
        torch.nn.ReLU(),
        torch.nn.Dropout(0.5),
        torch.nn.Linear(128, 4)  # 클래스 수에 맞게 출력 설정
    )
    base_model.load_state_dict(torch.load('/home/jajucha/mbn_model/best_model.pth'))  # 저장된 모델 가중치 로드
    base_model = base_model.to(device)
    base_model.eval()  # 평가 모드로 설정

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
    elif 171 not in V and V[3] < 130 and V[6] < 145 and (sum(L_V_set) < sum(R_V_set)):
        mode = "R_curve"
        Last_mode = "R_curve"
    elif 171 not in V and V[3] < 130 and V[1] < 145 and (sum(L_V_set) > sum(R_V_set)):
        mode = "L_curve"
        Last_mode = "L_curve"
    elif 171 not in V and V[3] < 144 and (sum(L_V_set) < sum(R_V_set)):
        mode = "R_blank_curve"
        Last_mode = "R_blank_curve"
    elif 171 not in V and V[3] < 144 and (sum(L_V_set) > sum(R_V_set)):
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
    
    
    if sum(d_set) > 150 and contact_count == 0:
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
        
    elif (d[0] > 40) and (sum(d_set) > 140) and contact_count == 1:
        right_arm = 0
        left_arm = 0
        velocity = -5
        jajucha2.control.set_motor(right_arm, left_arm, velocity)
        time.sleep(2)
        right_arm = 10
        left_arm = 10
        velocity = 3
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(2.7)
        right_arm = 0
        left_arm = 0
        velocity = 5
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(1.4)
        Last_mode = "straight"
        mode = "straight"
        contact_count += 1
    elif sum(d_set) > 110 and contact_count == 2:
        right_arm = 0
        left_arm = 0
        velocity = -3
        jajucha2.control.set_motor(right_arm, left_arm, velocity)
        time.sleep(2)
        right_arm = -10
        left_arm = -10
        velocity = 3
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(2.5)
        right_arm = 0
        left_arm = 0
        velocity = 3
        jajucha2.control.set_motor(right_arm, left_arm, velocity)
        time.sleep(1.5)
        right_arm = 9
        left_arm = 9
        velocity = 3
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        time.sleep(2)
        Last_mode = "R_curve"
        mode = "R_curve"
        jajucha2.control.stop_motor()
        contact_count += 1
        val1 += 1
    
    while val3 >= 1:
        image = jajucha2.camera.get_image('center')
        (V,L,R) ,grid = jajucha2.camera.gridFront(image)
        jajucha2.camera.show_image(grid)
        Red, Green, Blue = traffic_light(image,155,80,160,40)
    
        #print(mean_of_top_20)
        # V[3]을 기준으로 왼쪽 오른쪽 나눈 V값들
        L_V_set = [V[0],V[1],V[2]]
        R_V_set = [V[4],V[5],V[6]]
    
        # straight - 중앙추종 
        T_center = 320 - (L[2] - R[2])
        steering_const = 0.04
        steering = (320 - T_center) * steering_const
        steering = int(round(steering))

        # 이미지 전처리
        data_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        pil_image = Image.fromarray(s_image)
        img = data_transforms(pil_image).unsqueeze(0).to(device)  # 배치 차원 추가

        
        if V[3] == 171 and abs(((L[1] + R[1])/2 + (L[0] + R[0])/2) - 440) < 100:
            mode = "straight"
            Last_mode = "straight"
        if V[3] <= 155:
            velocity = 0
            with torch.no_grad():
                outputs = base_model(img)
                _, predicted = torch.max(outputs, 1)  # 가장 높은 확률을 가진 클래스를 선택

            # 클래스 이름 매핑 (클래스 인덱스에서 이름을 찾는 방법)
            class_names = os.listdir('/home/jajucha/img_data')
            predicted_class = class_names[predicted.item()]

            if predicted_class == "r":
                jajucha2.control.stop_motor()
            elif predicted_class == "rl":
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
            elif predicted_class == "g":
                right_arm = 0
                left_arm = 0
                velocity = 6
                jajucha2.control.set_motor(left_arm, right_arm, velocity)
                time.sleep(3)
                jajucha2.control.stop_motor()
            elif predicted_class == "p":
                right_arm = 0
                left_arm = 0
                velocity = -4
                jajucha2.control.set_motor(left_arm, right_arm, velocity)
                time.sleep(2)
                right_arm = -9
                left_arm = -9
                velocity = 4
                jajucha2.control.set_motor(left_arm, right_arm, velocity)
                time.sleep(1.5)
                jajucha2.control.stop_motor()
        
        
        if mode == 'straight':
            if V[3] <= 167:
                left_arm = -steering
                right_arm = -steering
                velocity = 4
            else:
                left_arm = -steering
                right_arm = -steering
                velocity = 5
                
        jajucha2.control.set_motor(left_arm, right_arm, velocity)
        
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
    
    #print(f"mode:{mode}, left_arm: {left_arm}, right_arm: {right_arm}, velocity: {velocity}")
    
    print(time_val)
    
    jajucha2.control.set_motor(left_arm, right_arm, velocity)
    
    mode = "default"
    
