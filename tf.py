import cv2
import numpy as np

# 특정 색상 범위 필터링 함수
def filter_color(image, lower_bound, upper_bound):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    return mask

# 빨간 원 감지 함수
def detect_red_circle(frame):
    red_mask = filter_color(frame, np.array([0, 100, 100]), np.array([10, 255, 255])) # 빨간색 HSV 범위
    print(red_mask)
    
# 초록 화살표 감지 함수
def detect_green_arrow(frame):
    green_mask = filter_color(frame, np.array([40, 50, 50]), np.array([80, 255, 255])) # 초록색 HSV 범위
    print(green_mask)
    
    
    
    
    
    
    import cv2
import numpy as np

# 특정 위치 기반 필터링 함수
def filter_color_in_region(image, lower_bound, upper_bound, x_start, x_end, y_start, y_end):
    # 관심 영역 (ROI) 설정
    roi = image[y_start:y_end, x_start:x_end]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    return mask

# 빨간 원 감지 함수 (왼쪽 영역)
def detect_red_circle_in_left(frame):
    # 왼쪽 영역 필터링
    red_mask = filter_color_in_region(frame, np.array([0, 100, 100]), np.array([10, 255, 255]), 0, 320, 0, 480)
    circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=50, param1=100, param2=30, minRadius=10, maxRadius=50)
    return circles is not None  # 원이 감지되면 True 반환

# 초록 화살표 감지 함수 (오른쪽 영역)
def detect_green_arrow_in_right(frame):
    # 오른쪽 영역 필터링
    green_mask = filter_color_in_region(frame, np.array([40, 50, 50]), np.array([80, 255, 255]), 320, 640, 0, 480)
   

    
    
    
    import jajucha2

while True:

    image = jajucha2.camera.get_image('center')
    (V,L,R) ,grid = jajucha2.camera.gridFront(image)
    jajucha2.camera.show_image(grid)

    detect_green_arrow(image)
    detect_red_circle(image)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    import cv2
import numpy as np

# 특정 색상 범위 필터링 함수
def filter_color(image, lower_bound, upper_bound):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    return mask

# 빨간 원 감지 함수
def detect_red_circle(frame):
    red_mask = filter_color(frame, np.array([0, 100, 100]), np.array([10, 255, 255])) # 빨간색 HSV 범위

    
# 초록 화살표 감지 함수
def detect_green_arrow(frame):
    green_mask = filter_color(frame, np.array([40, 50, 50]), np.array([80, 255, 255])) # 초록색 HSV 범위
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 7:  # 화살표 형태를 검출하기 위한 조건 (대략적인 조건)
            return True
    return False

# 메인 신호등 감지 함수
def detect_traffic_light_signal(frame):
    if detect_red_circle(frame):
        print("빨간 원 감지 - 정지 신호")
    elif detect_green_arrow(frame):
        print("초록 화살표 감지- 이동 신호")
    else:
        print("신호 감지 안됨")
