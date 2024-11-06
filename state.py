import jajucha2
import time
import cv2

steer = 0
speed = 0
mode = "straight"
Last_mode = "straight"

while True:
    image = jajucha2.camera.get_image('center')
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)
    
    L_V_set = [V[0],V[1],V[2]]
    R_V_set = [V[4],V[5],V[6]]

    print(f"V0: {V[0]}, V1: {V[1]}, V2: {V[2]}, V3: {V[3]}, V4: {V[4]}, V5: {V[5]}, V6: {V[6]}")
    


    if (sum(R_V_set) < sum(L_V_set)) and ((abs(V[0] - V[1]) + abs(V[1] - V[2]) + abs(V[0] - V[2])) / 3 < 7):
        