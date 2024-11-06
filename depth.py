import jajucha2
import cv2
import numpy as np
import asyncio
import time

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

while True:
    d = depth()
    d_set = [d[0],d[1],d[2]]
    image = jajucha2.camera.get_image('center')
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)

    print(d)
    left_arm = 0
    right_arm = 0
    velocity = 3
    
    if sum(d_set) >= 100:
        left_arm = -9
        right_arm = -9
        velocity = 3
        
        #jajucha2.control.set_motor(6, 6, 4)
        #time.sleep(1)
        
    jajucha2.control.set_motor(left_arm, right_arm, velocity)

